from dataclasses import dataclass
import random


@dataclass
class ClassificationResult:
    crop_type: str
    growth_stage: str
    confidence: float


def predict_crop_and_stage(_image_path: str) -> ClassificationResult:
    crops = ["wheat", "paddy", "soybean", "cotton"]
    stages = ["BBCH_10", "BBCH_30", "BBCH_50", "BBCH_70"]
    return ClassificationResult(
        crop_type=random.choice(crops),
        growth_stage=random.choice(stages),
        confidence=round(random.uniform(0.85, 0.98), 3),
    )
