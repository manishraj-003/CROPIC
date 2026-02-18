def damage_ratio_from_counts(healthy_pixels: int, damaged_pixels: int) -> float:
    total = healthy_pixels + damaged_pixels
    if total <= 0:
        return 0.0
    return round(damaged_pixels / total, 4)
