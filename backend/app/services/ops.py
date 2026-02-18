from collections import defaultdict, deque
from typing import Any


class LatencyStats:
    def __init__(self, max_samples: int = 500) -> None:
        self.max_samples = max_samples
        self.samples: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=max_samples))

    def add(self, path: str, millis: float) -> None:
        self.samples[path].append(millis)

    def snapshot(self) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for path, values in self.samples.items():
            if not values:
                continue
            sorted_vals = sorted(values)
            n = len(sorted_vals)
            p95_idx = max(int(n * 0.95) - 1, 0)
            output[path] = {
                "count": n,
                "avg_ms": round(sum(sorted_vals) / n, 2),
                "p95_ms": round(sorted_vals[p95_idx], 2),
                "max_ms": round(sorted_vals[-1], 2),
            }
        return output


latency_stats = LatencyStats()
