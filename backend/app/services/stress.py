def compute_ground_stress(damage_ratio: float, ndvi_hint: float | None = None) -> float:
    # Blend segmentation-derived damage with optional NDVI hint.
    stress = damage_ratio
    if ndvi_hint is not None:
        normalized = (1 - ((ndvi_hint + 1) / 2))  # higher stress for lower NDVI
        stress = (0.7 * damage_ratio) + (0.3 * normalized)
    if stress < 0:
        return 0.0
    if stress > 1:
        return 1.0
    return round(stress, 3)
