import json
from pathlib import Path
import subprocess

RUNS = 10
OUT = Path("docs/execution/demo_reliability_report.json")


def main() -> int:
    successes = 0
    failures = 0
    for _ in range(RUNS):
        proc = subprocess.run(["python", "scripts/smoke_backend_flow.py"], capture_output=True, text=True)
        if proc.returncode == 0:
            successes += 1
        else:
            failures += 1

    rate = successes / RUNS if RUNS else 0.0
    report = {
        "runs": RUNS,
        "successes": successes,
        "failures": failures,
        "success_rate": rate,
        "pass_threshold_0_9": rate >= 0.9,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["pass_threshold_0_9"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
