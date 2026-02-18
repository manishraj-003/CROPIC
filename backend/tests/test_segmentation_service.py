from app.services.segmentation import damage_ratio_from_counts


def test_damage_ratio_from_counts():
    assert damage_ratio_from_counts(80, 20) == 0.2
    assert damage_ratio_from_counts(0, 0) == 0.0
