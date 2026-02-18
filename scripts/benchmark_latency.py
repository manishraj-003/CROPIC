# Simple local latency benchmark helper.

import time
import requests

BASE = "http://localhost:8000"
ITER = 20


def measure(path: str) -> None:
    times = []
    for _ in range(ITER):
        start = time.perf_counter()
        requests.get(f"{BASE}{path}", timeout=3)
        end = time.perf_counter()
        times.append((end - start) * 1000)

    avg = sum(times) / len(times)
    p95 = sorted(times)[int(len(times) * 0.95) - 1]
    print(f"{path} avg={avg:.2f}ms p95={p95:.2f}ms")


if __name__ == "__main__":
    measure("/health")
