# NDVI and discrepancy simulation for claim CSV input.

from pathlib import Path
import csv
import random

IN_PATH = Path("claims_input.csv")
OUT_PATH = Path("claims_ndvi_output.csv")

if not IN_PATH.exists():
    print("claims_input.csv not found. Create with claim_id,ground_stress")
    raise SystemExit(1)

rows = []
with IN_PATH.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ndvi = round(random.uniform(0.1, 0.9), 3)
        ground = float(row["ground_stress"])
        delta = abs(ground - ndvi)
        row["satellite_ndvi"] = ndvi
        row["delta"] = round(delta, 3)
        row["flag_manual_audit"] = "yes" if delta > 0.3 else "no"
        rows.append(row)

with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {OUT_PATH}")
