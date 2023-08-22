from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from api.main import app, calculate_percent_overlap, create_db_connection
from api.types import DesignationType, FeatureClass, ManagerType

client = TestClient(app)


from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_db_connection(monkeypatch):
    mock_conn = MagicMock()
    monkeypatch.setattr("api.main.create_db_connection", lambda: mock_conn)
    return mock_conn


@pytest.fixture
def mock_calculate_percent_overlap(monkeypatch):
    monkeypatch.setattr(
        "api.main.calculate_percent_overlap", lambda *args, **kwargs: 70.0
    )


VALID_GEOMETRY = {
    "geometry": {
        "type": "Polygon",
        "coordinates": [[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]],
    }
}


def test_calculate_overlap_success(mock_db_connection, mock_calculate_percent_overlap):
    response = client.post("/percent_overlap/", json=VALID_GEOMETRY)
    assert response.status_code == 200
    assert response.json() == {"percent_overlap": 70.0}


def test_calculate_overlap_invalid_geojson(
    mock_db_connection, mock_calculate_percent_overlap
):
    response = client.post(
        "/percent_overlap/",
        json={
            "geometry": {"type": "InvalidType", "coordinates": [[0.0, 0.0], [1.0, 0.0]]}
        },
    )
    assert response.status_code == 400
    assert "Invalid GeoJSON data" in response.text


@pytest.mark.parametrize(
    "param_name, param_value",
    [
        ("manager_type", ManagerType.DIST.value),
        ("feature_class", FeatureClass.Designation.value),
        ("designation_type", DesignationType.CONE.value),
    ],
)
def test_calculate_overlap_with_query_parameters(
    mock_db_connection, mock_calculate_percent_overlap, param_name, param_value
):
    response = client.post(
        f"/percent_overlap/?{param_name}={param_value}", json=VALID_GEOMETRY
    )
    assert response.status_code == 200
    assert response.json() == {"percent_overlap": 70.0}


def test_calculate_overlap_with_combination_of_query_parameters(
    mock_db_connection, mock_calculate_percent_overlap
):
    query_params = f"?manager_type={ManagerType.FED.value}&feature_class={FeatureClass.Marine.value}&designation_type={DesignationType.FORE.value}"
    response = client.post(f"/percent_overlap/{query_params}", json=VALID_GEOMETRY)
    assert response.status_code == 200
    assert response.json() == {"percent_overlap": 70.0}


# Tests related to invalid query parameters
@pytest.mark.parametrize(
    "param_name, invalid_value",
    [
        ("manager_type", "invalid_type"),
        ("feature_class", "invalid_class"),
        ("designation_type", "invalid_designation"),
    ],
)
def test_calculate_overlap_invalid_query_parameters(
    mock_db_connection, mock_calculate_percent_overlap, param_name, invalid_value
):
    response = client.post(
        f"/percent_overlap/?{param_name}={invalid_value}", json=VALID_GEOMETRY
    )
    assert response.status_code == 422
    assert "Input should be" in response.text


if __name__ == "__main__":
    pytest.main([__file__])
