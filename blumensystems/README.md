# USGS PAD AOI API

Task: API to calculate coverage of a geojson AOI over USGS PAD sites. Filterable by Manager Type, Designation Type, and Feature Class

## Quick Start

This API is deployed on GCP Cloud Run. Accessible through - 

Please see the interactive redocs - 

### Example:

#### Yellowstone

Should be around 100% coverage

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/percent_overlap/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "geometry": {
        "coordinates": [
          [
            [
              -110.71005817035262,
              44.63959215763896
            ],
            [
              -110.71005817035262,
              44.543319225251366
            ],
            [
              -110.57148840601266,
              44.543319225251366
            ],
            [
              -110.57148840601266,
              44.63959215763896
            ],
            [
              -110.71005817035262,
              44.63959215763896
            ]
          ]
        ],
        "type": "Polygon"
      }
}'
```

##### SF 

Should be around 0 coverage

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/percent_overlap/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "geometry": {
        "coordinates": [
          [
            [
              -122.51952007335844,
              37.785897369700905
            ],
            [
              -122.51952007335844,
              37.694300515670434
            ],
            [
              -122.37165352299365,
              37.694300515670434
            ],
            [
              -122.37165352299365,
              37.785897369700905
            ],
            [
              -122.51952007335844,
              37.785897369700905
            ]
          ]
        ],
        "type": "Polygon"
      }
}'
```

## Local Quick Start

1. Download USGS PAD CONUS db

2. Load data into DB

```bash
backend/scripts/2-load_data.sh
```

3. Build the Dockerfile

```bash
backend/scripts/build_image.sh
```
4. Run image

```bash
docker run -p 8000:8000 blumensystems-pad-backend:latest
```

5. Check the interactive docs 

http://0.0.0.0:8000/docs

## Notes

- noteworthy script are in `backend/scripts`
- data is stored in a SpatiaLite database baked into the docker image
- this was ~3 hours of work, there is much to iterate on