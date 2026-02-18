import csv
from pathlib import Path

BASELINE = Path("data/metadata/baseline_label_distribution.csv")
CURRENT = Path("data/metadata/current_label_distribution.csv")
OUT = Path("docs/execution/drift_report.txt")
THRESHOLD = 0.15


def read_dist(path: Path) -> dict[str, float]:
    if not path.exists():
        return {}
    data: dict[str, float] = {}
    with path.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data[row["label"]] = float(row["ratio"])
    return data


def main() -> int:
    baseline = read_dist(BASELINE)
    current = read_dist(CURRENT)
    labels = sorted(set(baseline) | set(current))

    lines = ["Drift Report", "==========="]
    drifted = []
    for label in labels:
        b = baseline.get(label, 0.0)
        c = current.get(label, 0.0)
        delta = abs(c - b)
        flag = delta >= THRESHOLD
        lines.append(f"{label}: baseline={b:.3f} current={c:.3f} delta={delta:.3f} flag={flag}")
        if flag:
            drifted.append((label, delta))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved {OUT}")
    if drifted:
        print("Drift exceeded threshold for labels:", ", ".join(l for l, _ in drifted))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
