import numpy as np


def compute_damage_ratio(mask: np.ndarray) -> float:
    # Expected mask: 0=background, 1=healthy, 2=damaged
    plant_pixels = np.isin(mask, [1, 2]).sum()
    if plant_pixels == 0:
        return 0.0
    damaged_pixels = (mask == 2).sum()
    return float(damaged_pixels / plant_pixels)
