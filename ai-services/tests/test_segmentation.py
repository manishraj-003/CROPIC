import numpy as np
from src.segmentation import compute_damage_ratio


def test_damage_ratio():
    mask = np.array([
        [0, 1, 1],
        [2, 2, 1],
        [0, 0, 2],
    ])
    ratio = compute_damage_ratio(mask)
    assert abs(ratio - 0.5) < 1e-9
