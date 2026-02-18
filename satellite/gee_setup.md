# Google Earth Engine Setup Notes

## Objective
Fetch Sentinel-2 data for pilot districts and compute NDVI for claim coordinates.

## Steps
1. Create GEE account and enable API access.
2. Define AOI polygons for pilot districts.
3. Query Sentinel-2 SR dataset by date and cloud threshold.
4. Compute NDVI using: (NIR - RED) / (NIR + RED).
5. Export NDVI summaries by farm/claim coordinates.

## Output Contract
- claim_id
- latitude
- longitude
- observation_date
- ndvi_value
- cloud_cover
- source_scene_id
