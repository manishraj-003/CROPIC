import json
from pathlib import Path
import sys

REPORT = Path("docs/execution/load_test_report.json")
THRESHOLD_MS = 2000.0


def main() -> int:
    if not REPORT.exists():
        print("Missing load test report. Run scripts/load_test_backend.py first.")
        return 1

    data = json.loads(REPORT.read_text(encoding="utf-8"))
    results = data.get("results", {})
    failed = []
    for name, metrics in results.items():
        p95 = float(metrics.get("p95_ms", 999999))
        if p95 >= THRESHOLD_MS:
            failed.append((name, p95))

    if failed:
        print("Latency gate failed:")
        for name, p95 in failed:
            print(f"- {name}: p95={p95}ms >= {THRESHOLD_MS}ms")
        return 2

    print("Latency gate passed for all measured endpoints.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
