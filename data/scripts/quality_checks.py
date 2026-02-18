from pathlib import Path
import csv

MANIFEST = Path(__file__).resolve().parents[1] / "metadata" / "dataset_manifest.csv"


def main() -> None:
    if not MANIFEST.exists():
        print("Manifest not found. Run build_manifest.py first.")
        return

    with MANIFEST.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    missing_label = sum(1 for r in rows if not r.get("disease_or_stress_label"))
    unknown_crop = sum(1 for r in rows if r.get("crop_type", "").strip().lower() == "unknown")

    print(f"rows={len(rows)}")
    print(f"missing_label={missing_label}")
    print(f"unknown_crop={unknown_crop}")


if __name__ == "__main__":
    main()
