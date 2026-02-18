from app.services.classifier import classify_crop_and_stage
from app.services.stress import compute_ground_stress


def test_classifier_returns_valid_ranges():
    crop, stage, confidence = classify_crop_and_stage("IMG-1")
    assert crop in {"wheat", "paddy", "cotton", "soybean"}
    assert stage in {"BBCH_10", "BBCH_30", "BBCH_50", "BBCH_70"}
    assert 0.85 <= confidence <= 0.99


def test_ground_stress_blend():
    score = compute_ground_stress(0.5, 0.4)
    assert 0 <= score <= 1
