from app.services.ndvi import synthetic_ndvi


def test_synthetic_ndvi_range():
    value = synthetic_ndvi(23.12, 77.42, "2026-02-18")
    assert -1 <= value <= 1
