from __future__ import annotations
from cgi import print_arguments

import logging
import sqlite3
import threading

import cachetools
import dotenv
import fastapi
import pydantic_settings
from pydantic import BaseModel
from shapely.geometry import shape

from api import types

dotenv.load_dotenv()


class Settings(pydantic_settings.BaseSettings):
    DATABASE_URL: str
    CACHE_MAX_SIZE: int = 100
    CACHE_TTL_SECONDS: int = 300


settings = Settings()

app = fastapi.FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cache = cachetools.TTLCache(
    maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL_SECONDS
)


class AreaOfInterest(BaseModel):
    """
    Pydantic model for an Area of Interest (AOI) represented as GeoJSON.
    """

    geometry: dict


class PercentOverlapResponse(BaseModel):
    """
    Response model for the percent overlap calculation result.
    """

    percent_overlap: float


def create_db_connection() -> sqlite3.Connection:
    """
    Create a SQLite database connection with spatialite extension enabled.

    Returns:
        sqlite3.Connection: A database connection.
    """
    conn = sqlite3.connect(settings.DATABASE_URL, check_same_thread=False)
    conn.enable_load_extension(True)
    conn.load_extension("mod_spatialite")
    return conn


thread_local = threading.local()


def get_db() -> sqlite3.Connection:
    """
    Get a thread-local SQLite database connection.

    Returns:
        sqlite3.Connection: A database connection.
    """
    if not hasattr(thread_local, "conn"):
        thread_local.conn = create_db_connection()
    return thread_local.conn


@cachetools.cached(cache)
def calculate_percent_overlap(
    aoi_wkt: str,
    conn: sqlite3.Connection,
    manager_type: types.ManagerType | None = None,
    feature_class: types.FeatureClass | None = None,
    designation_type: types.DesignationType | None = None,
) -> float:
    """
    Calculate the percent overlap of an Area of Interest (AOI) with spatial data in the database.

    Args:
        aoi_wkt (str): Well-known text representation of the AOI geometry (EPSG:4326).
        conn (sqlite3.Connection): SQLite database connection.
        manager_type (ManagerType, optional): Enum value for manager type.
        feature_class (FeatureClass, optional): Enum value for feature class.
        designation_type (DesignationType, optional): Enum value for designation type.

    Returns:
        float: Percent overlap value.
    """
    cursor = conn.cursor()

    logging.debug(f"{aoi_wkt=}")

    # Transform AOI to EPSG:5070 from 4326 (assumed)
    cursor.execute(
        f"SELECT ST_Area(ST_Transform(GeomFromText('{aoi_wkt}', 4326), 5070))"
    )
    aoi_area = cursor.fetchone()[0]

    logging.debug(f"{aoi_area=}")

    where_conditions = [
        "ROWID IN (SELECT ROWID FROM SpatialIndex WHERE f_table_name = 'usgs_pad' AND search_frame = ST_Transform(GeomFromText(?, 4326), 5070))"
    ]
    params = [aoi_wkt, aoi_wkt]

    if manager_type:
        where_conditions.append(f"{types.MANAGER_TYPE_COL_NAME} = ?")
        params.append(manager_type.name)

    if feature_class:
        where_conditions.append(f"{types.FEATURE_CLASS_COL_NAME} = ?")
        params.append(feature_class.name)

    if designation_type:
        where_conditions.append(f"{types.DESIGNATION_TYPE_COL_NAME} = ?")
        params.append(designation_type.name)

    
    print(f"SQL parameters: {params}")


    cursor.execute(
        f"""
        SELECT SUM(ST_Area(ST_Intersection(ST_Transform(GeomFromText(?, 4326), 5070), shape)))
        FROM usgs_pad
        WHERE {' AND '.join(where_conditions)}
        """,
        params,
    )
    overlap_area = cursor.fetchone()[0]

    if overlap_area is None or overlap_area == 0:
        logging.debug("No overlap found")
        print("No overlap")
        return 0.0

    logging.debug(f"{overlap_area=}")

    percent_overlap = (overlap_area / aoi_area) * 100.0

    return min(percent_overlap, 100)


example_geojson = {
    "geometry": {
        "type": "Polygon",
        "coordinates": [[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]],
    }
}


@app.post(
    "/percent_overlap/",
    responses={
        400: {"description": "Invalid GeoJSON data"},
    },
    response_model=PercentOverlapResponse,
)
async def calculate_overlap(
    aoi_geojson: AreaOfInterest = fastapi.Body(examples=example_geojson),
    manager_type: types.ManagerType = fastapi.Query(None),
    feature_class: types.FeatureClass = fastapi.Query(None),
    designation_type: types.DesignationType = fastapi.Query(None),
    conn: sqlite3.Connection = fastapi.Depends(get_db),
) -> PercentOverlapResponse:
    """
    Calculate the percent overlap of the provided Area of Interest (AOI) with spatial data.

    Args:
        aoi_geojson (AreaOfInterest): Input AOI geometry in GeoJSON format.
        conn (sqlite3.Connection): SQLite database connection.
        manager_type (ManagerType, optional): Enum value for manager type.
        feature_class (FeatureClass, optional): Enum value for feature class.
        designation_type (DesignationType, optional): Enum value for designation type.

    Returns:
        PercentOverlapResponse: Calculated percent overlap.
    """
    try:
        aoi_geometry = shape(aoi_geojson.geometry)
    except Exception as e:
        logging.exception("Failed to parse AOI")
        raise fastapi.HTTPException(status_code=400, detail="Invalid GeoJSON data.")

    if not aoi_geometry.is_valid:
        raise fastapi.HTTPException(status_code=400, detail="Invalid GeoJSON data.")

    aoi_wkt = aoi_geometry.wkt

    percent_overlap = calculate_percent_overlap(
        aoi_wkt,
        conn,
        manager_type=manager_type,
        feature_class=feature_class,
        designation_type=designation_type,
    )
    return PercentOverlapResponse(percent_overlap=percent_overlap)
