import json
from pathlib import Path

LOAD = Path("docs/execution/load_test_report.json")
METRICS = Path("docs/execution/success_metrics_report.txt")
DRIFT = Path("docs/execution/drift_report.txt")


def main() -> None:
    print("CROPIC Check Summary")
    print("====================")

    if LOAD.exists():
        data = json.loads(LOAD.read_text(encoding="utf-8"))
        print("Load Test:")
        for name, metrics in data.get("results", {}).items():
            print(
                f"- {name}: avg={metrics.get('avg_ms')}ms "
                f"p95={metrics.get('p95_ms')}ms pass_under_2s={metrics.get('pass_under_2s')}"
            )
    else:
        print("Load Test: report missing")

    if METRICS.exists():
        print("\nSuccess Metrics:")
        print(METRICS.read_text(encoding="utf-8").strip())
    else:
        print("\nSuccess Metrics: report missing")

    if DRIFT.exists():
        print("\nDrift:")
        lines = DRIFT.read_text(encoding="utf-8").strip().splitlines()
        for line in lines[:8]:
            print(line)
        if len(lines) > 8:
            print("...")
    else:
        print("\nDrift: report missing")


if __name__ == "__main__":
    main()
