import hashlib
from functools import lru_cache


@lru_cache(maxsize=4096)
def synthetic_ndvi(latitude: float, longitude: float, observation_date: str | None = None) -> float:
    seed = f"{latitude:.5f}:{longitude:.5f}:{observation_date or ''}"
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    raw = int(digest[:8], 16) / 0xFFFFFFFF
    ndvi = (raw * 1.2) - 0.2  # map to roughly [-0.2, 1.0]
    if ndvi < -1:
        return -1.0
    if ndvi > 1:
        return 1.0
    return round(ndvi, 3)
