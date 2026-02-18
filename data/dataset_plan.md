# Dataset Plan (Phase 1)

## Target
- 50,000 curated images for baseline model training.

## Sources
- PlantVillage
- DLCPD-25
- Mendeley Data

## Curation Rules
- Remove duplicates and near-duplicates.
- Normalize resolution and format.
- Track source license and attribution.
- Keep class balance log.

## Folder Convention
- `raw/<source>/<class>/...`
- `processed/<task>/<split>/...`
- `metadata/dataset_manifest.csv`

## Minimum Metadata Fields
- image_id
- source
- crop_type
- disease_or_stress_label
- growth_stage (if available)
- split (train/val/test)
- license
