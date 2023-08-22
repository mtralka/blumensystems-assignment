# USGS PAD AOI API

Task: API to calculate coverage of a geojson AOI over USGS PAD sites. Filterable by Manager Type, Designation Type, and Feature Class

## Quick Start

This API is deployed on GCP Cloud Run. Accessible through - https://usgs-pad-api-n2cxkwenpq-uc.a.run.app

Please see the interactive redocs - https://usgs-pad-api-n2cxkwenpq-uc.a.run.app/docs. You can interact with the API fully through this interface. I recomend http://geojson.io to generate AOIs

### Example:

#### SF Bay Marine Area

Should be 100% coverage

```bash
curl -X 'POST' \
  'https://usgs-pad-api-n2cxkwenpq-uc.a.run.app/percent_overlap/?feature_class=Marine' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "geometry": {
        "coordinates": [
          [
            [
              -125.42999123368182,
              37.989737811537594
            ],
            [
              -125.42999123368182,
              36.5091296339357
            ],
            [
              -123.35737871186768,
              36.5091296339357
            ],
            [
              -123.35737871186768,
              37.989737811537594
            ],
            [
              -125.42999123368182,
              37.989737811537594
            ]
          ]
        ],
        "type": "Polygon"
      }
}'
```

Change Feature Class and note 0% coverage

```
feature_class=Fee
```

##### YellowStone Private Entities

Should be 0 coverage

```bash
curl -X 'POST' \
  'https://usgs-pad-api-n2cxkwenpq-uc.a.run.app/percent_overlap/?manager_type=Private%20Entity' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "geometry": {
        "coordinates": [
          [
            [
              -110.8136743303338,
              44.67864029426991
            ],
            [
              -110.8136743303338,
              44.48725748685462
            ],
            [
              -110.54138379334174,
              44.48725748685462
            ],
            [
              -110.54138379334174,
              44.67864029426991
            ],
            [
              -110.8136743303338,
              44.67864029426991
            ]
          ]
        ],
        "type": "Polygon"
      }
}'
```

...because Yellowstone is 100% Federally owned

```bash
curl -X 'POST' \
  'https://usgs-pad-api-n2cxkwenpq-uc.a.run.app/percent_overlap/?manager_type=Federal%20Government&designation_type=National%20Park' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "geometry": {
        "coordinates": [
          [
            [
              -110.8136743303338,
              44.67864029426991
            ],
            [
              -110.8136743303338,
              44.48725748685462
            ],
            [
              -110.54138379334174,
              44.48725748685462
            ],
            [
              -110.54138379334174,
              44.67864029426991
            ],
            [
              -110.8136743303338,
              44.67864029426991
            ]
          ]
        ],
        "type": "Polygon"
      }
}'
```

## Local Quick Start

1. Download CONUS USGS PAD GDB

https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-download

2. Load data into DB

```bash
./backend/scripts/2-load_data.sh
```

3. Build the Dockerfile

```bash
./backend/scripts/build_image.sh
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