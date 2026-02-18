import csv
import json
from pathlib import Path

MANIFEST = Path("data/metadata/dataset_manifest_split.csv")
MANIFEST_FALLBACK = Path("data/metadata/dataset_manifest.csv")
OUT = Path("ai-services/artifacts/classifier_baseline.json")


def main() -> None:
    source = MANIFEST if MANIFEST.exists() else MANIFEST_FALLBACK
    if not source.exists():
        raise SystemExit("Missing dataset manifest. Run data/scripts/build_manifest.py first.")

    by_image = {}
    with source.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_id = row["image_id"]
            label = row.get("crop_type", "unknown") or "unknown"
            by_image[image_id] = label

    payload = {
        "model_name": "classifier-baseline-v1",
        "num_samples": len(by_image),
        "index": by_image,
        "default_crop": "wheat",
        "default_growth_stage": "BBCH_30",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload), encoding="utf-8")
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
