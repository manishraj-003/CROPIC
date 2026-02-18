from pathlib import Path
import csv
import random

MANIFEST = Path(__file__).resolve().parents[1] / "metadata" / "dataset_manifest.csv"
OUT = Path(__file__).resolve().parents[1] / "metadata" / "dataset_manifest_split.csv"


def assign_split(idx: int) -> str:
    # 70/15/15 deterministic split by row index.
    mod = idx % 20
    if mod < 14:
        return "train"
    if mod < 17:
        return "val"
    return "test"


def main() -> None:
    if not MANIFEST.exists():
        print("Manifest not found. Run build_manifest.py first.")
        return

    with MANIFEST.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    random.seed(42)
    random.shuffle(rows)

    for idx, row in enumerate(rows):
        row["split"] = assign_split(idx)

    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)

    print(f"Wrote split manifest: {OUT}")


if __name__ == "__main__":
    main()
