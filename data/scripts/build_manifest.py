# Data Manifest Builder

from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
OUT = ROOT / "metadata" / "dataset_manifest.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

rows = []
for image in RAW.rglob("*"):
    if image.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        continue
    parts = image.relative_to(RAW).parts
    source = parts[0] if len(parts) > 0 else "unknown"
    label = parts[1] if len(parts) > 1 else "unknown"

    rows.append(
        {
            "image_id": image.stem,
            "source": source,
            "crop_type": "unknown",
            "disease_or_stress_label": label,
            "growth_stage": "unknown",
            "split": "unassigned",
            "license": "check-source-license",
            "path": str(image),
        }
    )

with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [
        "image_id", "source", "crop_type", "disease_or_stress_label", "growth_stage", "split", "license", "path"
    ])
    writer.writeheader()
    if rows:
        writer.writerows(rows)

print(f"Wrote manifest: {OUT} ({len(rows)} rows)")
