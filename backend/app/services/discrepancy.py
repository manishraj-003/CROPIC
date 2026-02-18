def compute_discrepancy(ground_stress: float, satellite_ndvi: float) -> float:
    return abs(ground_stress - satellite_ndvi)


def should_flag(discrepancy: float, threshold: float = 0.3) -> bool:
    return discrepancy > threshold
