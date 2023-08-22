import os
import pathlib

import fiona
import geopandas as gpd
import numpy as np

##
# Step 1.
# Explore Data
#
# Explore the USGS PAD geodatabase.
##

designation_layer_name = "PADUS3_0Designation"
gdb_path = "PAD_US3_0.gdb"
gdb_path = "/home/mtralka/Documents/blumensystems/PAD_US3_0.gdb"

top_path = pathlib.Path(__file__).parent
app_path = top_path.parent
data_path = (app_path / "data").resolve()
gdb_path = data_path / "PAD_US3_0.gdb"

print("Layers in the Geodatabase:")
print(fiona.listlayers(gdb_path))

gdf = gpd.read_file(gdb_path, layer=designation_layer_name)

print("Column names:", gdf.columns)

median_area = np.median(gdf["GIS_Acres"])
min_area = np.min(gdf["GIS_Acres"])
max_area = np.max(gdf["GIS_Acres"])

# Designation stats (acres): median_area=174.0 min_area=0 max_area=372846083
print(f"Designation stats (acres): {median_area=} {min_area=} {max_area=}")

gdf["perimeter"] = gdf["geometry"].apply(lambda geom: geom.length)

complexity = gdf["GIS_Acres"] / gdf["perimeter"]
median_complexity = np.median(complexity)
min_complexity = np.min(complexity)
max_complexity = np.max(complexity)

# median_complexity=0.03402886379766241 min_complexity=0.0 max_complexity=52.05808406110619
print(
    f"Median Area / Perimeter Complexity (acres/meter): \
    {median_complexity=} {min_complexity=} {max_complexity=}"
)


print("Unique Manager types")
print(gdf["mang_types"].unique())

print("Unique feature clases")
print(gdf["featclass"].unique())

print("Unique designation type")
print(gdf["des_tp"].unique())
