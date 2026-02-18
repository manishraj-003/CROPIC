from datetime import datetime
from pydantic import BaseModel, Field


class UploadMetadata(BaseModel):
    user_id: str = Field(..., description="Farmer or FLW identifier")
    farm_id: str
    latitude: float
    longitude: float
    captured_at: datetime
    device_id: str
    blur_score: float | None = None
    language: str | None = None
    district: str | None = None
    village: str | None = None


class ClaimCreateRequest(BaseModel):
    claim_id: str
    farm_id: str
    user_id: str
    image_id: str


class DualVerificationRequest(BaseModel):
    claim_id: str
    ground_stress: float = Field(..., ge=0, le=1)
    satellite_ndvi: float = Field(..., ge=-1, le=1)


class DualVerificationResponse(BaseModel):
    claim_id: str
    discrepancy_score: float
    flagged_for_audit: bool


class TamperCheckRequest(BaseModel):
    claim_id: str
    image_path: str


class TamperCheckResponse(BaseModel):
    claim_id: str
    ela_score: float
    suspected_tamper: bool


class AuthTokenRequest(BaseModel):
    phone: str
    role: str = Field(default="flw")


class ClassificationRequest(BaseModel):
    image_id: str
    image_path: str | None = None


class ClassificationResponse(BaseModel):
    image_id: str
    crop_type: str
    growth_stage: str
    confidence: float


class StressScoreRequest(BaseModel):
    claim_id: str
    damage_ratio: float = Field(..., ge=0, le=1)
    ndvi_hint: float | None = Field(default=None, ge=-1, le=1)


class StressScoreResponse(BaseModel):
    claim_id: str
    ground_stress: float


class SegmentationRequest(BaseModel):
    image_id: str
    healthy_pixels: int = Field(..., ge=0)
    damaged_pixels: int = Field(..., ge=0)


class SegmentationResponse(BaseModel):
    image_id: str
    damage_ratio: float


class VoiceReportRequest(BaseModel):
    claim_id: str
    language: str
    transcript: str


class VoiceReportResponse(BaseModel):
    claim_id: str
    language: str
    normalized_transcript: str


class NdviRequest(BaseModel):
    claim_id: str
    latitude: float
    longitude: float
    observation_date: str | None = None


class NdviResponse(BaseModel):
    claim_id: str
    ndvi_value: float
    source: str
