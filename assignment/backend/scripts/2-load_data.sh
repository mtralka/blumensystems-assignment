#!/bin/bash

##
# Step 2.
# Load Data
#
# Load the USGS PAD data into SpatiaLite.
# OGR handles creating spatial indexes.
#
# We are transforming data into an equal-areas projection
# before loading - -t_srs
##

TOP="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$TOP")"
DATA_DIR="$APP_DIR/data/"

DATABASE_PATH="$DATA_DIR/db.sqlite"
GDB_PATH="$DATA_DIR/PAD_US3_0.gdb"

LAYERS=("PADUS3_0Designation"
        "PADUS3_0Easement"
        "PADUS3_0Fee"
        "PADUS3_0Marine"
        "PADUS3_0Proclamation"
        )

GDB_LAYER="PADUS3_0Combined_Proclamation_Marine_Fee_Designation_Easement"

ogr2ogr -f "SQLite" "$DATABASE_PATH" "$GDB_PATH" "$GDB_LAYER" -nln "usgs_pad" -dsco SPATIALITE=YES -t_srs "EPSG:5070" -skipfailures

echo "Data ingested into Spatialite database. Creating indexes"

ogr2ogr -f "SQLite" -dsco SPATIALITE=YES -update "$DATABASE_PATH" "$DATABASE_PATH" -dialect "SQLite" -sql "CREATE INDEX idx_mang_type ON usgs_pad(mang_type)"
ogr2ogr -f "SQLite" -dsco SPATIALITE=YES -update "$DATABASE_PATH" "$DATABASE_PATH" -dialect "SQLite" -sql "CREATE INDEX idx_des_tp ON usgs_pad(des_tp)"
ogr2ogr -f "SQLite" -dsco SPATIALITE=YES -update "$DATABASE_PATH" "$DATABASE_PATH" -dialect "SQLite" -sql "CREATE INDEX idx_featclass ON usgs_pad(featclass)"

echo "Done!"