import json
from pathlib import Path

LOAD = Path("docs/execution/load_test_report.json")
METRICS = Path("docs/execution/success_metrics_report.txt")
RELIABILITY = Path("docs/execution/demo_reliability_report.json")


def parse_metrics(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip()
    return data


def main() -> int:
    failures: list[str] = []

    if not LOAD.exists():
        failures.append("missing load_test_report.json")
    else:
        load = json.loads(LOAD.read_text(encoding="utf-8"))
        for name, m in load.get("results", {}).items():
            if not m.get("pass_under_2s", False):
                failures.append(f"latency gate failed for {name}")

    metrics = parse_metrics(METRICS)
    if metrics.get("classification_target_met") != "True":
        failures.append("classification target not met")
    if metrics.get("segmentation_target_met") != "True":
        failures.append("segmentation target not met")

    if not RELIABILITY.exists():
        failures.append("missing demo_reliability_report.json")
    else:
        rel = json.loads(RELIABILITY.read_text(encoding="utf-8"))
        if not rel.get("pass_threshold_0_9", False):
            failures.append("demo reliability < 90%")

    if failures:
        print("TRL gate failed:")
        for item in failures:
            print(f"- {item}")
        return 2

    print("TRL gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
