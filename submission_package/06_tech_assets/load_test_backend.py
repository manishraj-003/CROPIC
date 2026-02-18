import concurrent.futures
import json
from pathlib import Path
import time
from typing import Callable

import requests

BASE = "http://127.0.0.1:8000"
WORKERS = 20
REQUESTS = 200
P95_THRESHOLD_MS = 2000.0
OUT = Path("docs/execution/load_test_report.json")


def issue_token(role: str) -> str:
    r = requests.post(
        f"{BASE}/v1/auth/token",
        json={"phone": "9999999999", "role": role},
        timeout=5,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def hit_health() -> float:
    start = time.perf_counter()
    r = requests.get(f"{BASE}/health", timeout=3)
    r.raise_for_status()
    return (time.perf_counter() - start) * 1000


def hit_summary(token: str) -> float:
    start = time.perf_counter()
    r = requests.get(
        f"{BASE}/v1/dashboard/summary",
        headers={"Authorization": f"Bearer {token}"},
        timeout=3,
    )
    r.raise_for_status()
    return (time.perf_counter() - start) * 1000


def hit_upload(token: str) -> float:
    payload = {
        "user_id": "U1",
        "farm_id": "FARM-LOAD",
        "latitude": 23.12,
        "longitude": 77.42,
        "captured_at": "2026-02-18T10:00:00Z",
        "device_id": "DEV-LOAD",
        "language": "hi",
        "district": "karnal",
        "village": "v1",
    }
    start = time.perf_counter()
    r = requests.post(
        f"{BASE}/v1/images/metadata",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=3,
    )
    r.raise_for_status()
    return (time.perf_counter() - start) * 1000


def summarize_timings(timings: list[float]) -> dict:
    timings.sort()
    n = len(timings)
    avg = sum(timings) / n
    p95 = timings[int(n * 0.95) - 1]
    return {
        "avg_ms": round(avg, 2),
        "p95_ms": round(p95, 2),
        "max_ms": round(timings[-1], 2),
        "requests": n,
        "pass_under_2s": p95 < P95_THRESHOLD_MS,
    }


def run_load(fn: Callable[[], float]) -> dict:
    timings = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = [ex.submit(fn) for _ in range(REQUESTS)]
        for f in concurrent.futures.as_completed(futures):
            timings.append(f.result())
    return summarize_timings(timings)


if __name__ == "__main__":
    insurer_token = issue_token("insurer")
    flw_token = issue_token("flw")

    report = {
        "config": {"workers": WORKERS, "requests": REQUESTS, "threshold_ms": P95_THRESHOLD_MS},
        "results": {
            "health": run_load(hit_health),
            "dashboard_summary": run_load(lambda: hit_summary(insurer_token)),
            "metadata_upload": run_load(lambda: hit_upload(flw_token)),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    print(f"Saved {OUT}")
