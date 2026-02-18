import csv
import json
from pathlib import Path

SRC = Path("docs/execution/segmentation_eval.csv")
OUT = Path("ai-services/artifacts/segmentation_baseline.json")


def main() -> None:
    # Placeholder "training": stores default threshold and known calibration values.
    observed = []
    if SRC.exists():
        with SRC.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    observed.append((int(row["true_mask_bin"]), int(row["pred_mask_bin"])))
                except Exception:
                    continue

    payload = {
        "model_name": "segmentation-baseline-v1",
        "num_observed_pairs": len(observed),
        "damage_threshold": 0.5,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload), encoding="utf-8")
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
