from typing import Annotated

from time import perf_counter

from fastapi import Depends, FastAPI, HTTPException, Request

from app.config import settings
from app.schemas import (
    AuthTokenRequest,
    ClaimCreateRequest,
    ClassificationRequest,
    ClassificationResponse,
    DualVerificationRequest,
    DualVerificationResponse,
    StressScoreRequest,
    StressScoreResponse,
    SegmentationRequest,
    SegmentationResponse,
    TamperCheckRequest,
    TamperCheckResponse,
    UploadMetadata,
    VoiceReportRequest,
    VoiceReportResponse,
    NdviRequest,
    NdviResponse,
)
from app.services.audit import write_audit
from app.services.auth import create_access_token, get_current_user, require_roles
from app.services.classifier import classify_crop_and_stage
from app.services.discrepancy import compute_discrepancy, should_flag
from app.services.repository import SqliteRepository, build_repository
from app.services.stress import compute_ground_stress
from app.services.segmentation import damage_ratio_from_counts
from app.services.tamper import ela_score
from app.services.voice import SUPPORTED_LANGUAGES, is_supported_language, normalize_transcript
from app.services.ndvi import synthetic_ndvi
from app.services.ops import latency_stats

app = FastAPI(title="CROPIC-AI API", version="0.4.0")
repo = build_repository(settings.database_url)


@app.middleware("http")
async def record_latency(request: Request, call_next):
    start = perf_counter()
    response = await call_next(request)
    elapsed_ms = (perf_counter() - start) * 1000
    latency_stats.add(request.url.path, elapsed_ms)
    return response


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": settings.app_name,
        "env": settings.env,
        "version": "0.4.0",
        "database_url": settings.database_url,
    }


@app.post("/v1/auth/token")
def issue_token(payload: AuthTokenRequest) -> dict:
    token = create_access_token(subject=payload.phone, role=payload.role)
    write_audit("auth.token_issued", payload.phone, {"phone": payload.phone, "role": payload.role})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/v1/images/metadata")
def create_image_metadata(
    payload: UploadMetadata,
    user: Annotated[dict, Depends(require_roles("farmer", "flw", "admin"))],
) -> dict:
    record = repo.save_metadata(payload.model_dump())
    write_audit("images.metadata_created", user["subject"], {"farm_id": payload.farm_id})
    return {"message": "metadata accepted", "record": record}


@app.post("/v1/claims")
def create_claim_endpoint(
    payload: ClaimCreateRequest,
    user: Annotated[dict, Depends(require_roles("flw", "insurer", "admin"))],
) -> dict:
    record = repo.create_claim(payload.model_dump())
    write_audit("claims.created", user["subject"], {"claim_id": payload.claim_id})
    return {"message": "claim created", "record": record}


@app.post("/v1/ai/classify", response_model=ClassificationResponse)
def classify_image(
    payload: ClassificationRequest,
    user: Annotated[dict, Depends(require_roles("flw", "insurer", "admin"))],
) -> ClassificationResponse:
    crop, stage, confidence = classify_crop_and_stage(payload.image_id)
    write_audit("ai.classify", user["subject"], {"image_id": payload.image_id, "crop": crop, "stage": stage})
    return ClassificationResponse(
        image_id=payload.image_id,
        crop_type=crop,
        growth_stage=stage,
        confidence=confidence,
    )


@app.post("/v1/ai/stress", response_model=StressScoreResponse)
def estimate_stress(
    payload: StressScoreRequest,
    user: Annotated[dict, Depends(require_roles("flw", "insurer", "admin"))],
) -> StressScoreResponse:
    stress = compute_ground_stress(payload.damage_ratio, payload.ndvi_hint)
    write_audit("ai.stress", user["subject"], {"claim_id": payload.claim_id, "ground_stress": stress})
    return StressScoreResponse(claim_id=payload.claim_id, ground_stress=stress)


@app.post("/v1/ai/segment", response_model=SegmentationResponse)
def segment_damage(
    payload: SegmentationRequest,
    user: Annotated[dict, Depends(require_roles("flw", "insurer", "admin"))],
) -> SegmentationResponse:
    ratio = damage_ratio_from_counts(payload.healthy_pixels, payload.damaged_pixels)
    write_audit("ai.segment", user["subject"], {"image_id": payload.image_id, "damage_ratio": ratio})
    return SegmentationResponse(image_id=payload.image_id, damage_ratio=ratio)


@app.post("/v1/verification/dual", response_model=DualVerificationResponse)
def run_dual_verification(
    payload: DualVerificationRequest,
    user: Annotated[dict, Depends(require_roles("insurer", "admin", "flw"))],
) -> DualVerificationResponse:
    discrepancy = compute_discrepancy(payload.ground_stress, payload.satellite_ndvi)
    flagged = should_flag(discrepancy, settings.discrepancy_threshold)

    if isinstance(repo, SqliteRepository):
        repo.update_claim_discrepancy(payload.claim_id, discrepancy)

    if flagged:
        repo.add_audit_flag(
            {
                "claim_id": payload.claim_id,
                "discrepancy": discrepancy,
                "reason": "Ground/Satellite mismatch",
            }
        )

    write_audit(
        "verification.dual",
        user["subject"],
        {"claim_id": payload.claim_id, "discrepancy": discrepancy, "flagged": flagged},
    )
    return DualVerificationResponse(
        claim_id=payload.claim_id,
        discrepancy_score=discrepancy,
        flagged_for_audit=flagged,
    )


@app.get("/v1/audit/queue")
def get_audit_queue(user: Annotated[dict, Depends(require_roles("insurer", "admin"))]) -> dict:
    write_audit("audit.queue_viewed", user["subject"], {})
    return {"items": repo.list_audit_queue()}


@app.post("/v1/fraud/ela", response_model=TamperCheckResponse)
def run_tamper_check(
    payload: TamperCheckRequest,
    user: Annotated[dict, Depends(require_roles("insurer", "admin", "flw"))],
) -> TamperCheckResponse:
    try:
        score = ela_score(payload.image_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Image not found") from exc

    suspected = score > 5.0
    if suspected:
        repo.add_audit_flag(
            {
                "claim_id": payload.claim_id,
                "reason": "Potential tamper via ELA",
                "ela_score": score,
            }
        )

    write_audit(
        "fraud.ela_checked",
        user["subject"],
        {"claim_id": payload.claim_id, "ela_score": score, "suspected": suspected},
    )
    return TamperCheckResponse(claim_id=payload.claim_id, ela_score=score, suspected_tamper=suspected)


@app.get("/v1/dashboard/summary")
def dashboard_summary(user: Annotated[dict, Depends(require_roles("insurer", "admin", "flw"))]) -> dict:
    write_audit("dashboard.summary_viewed", user["subject"], {})
    return repo.summary()


@app.get("/v1/dashboard/clusters")
def dashboard_clusters(user: Annotated[dict, Depends(require_roles("insurer", "admin", "flw"))]) -> dict:
    write_audit("dashboard.clusters_viewed", user["subject"], {})
    return {"items": repo.clusters()}


@app.get("/v1/dashboard/regions")
def dashboard_regions(user: Annotated[dict, Depends(require_roles("insurer", "admin", "flw"))]) -> dict:
    write_audit("dashboard.regions_viewed", user["subject"], {})
    return {"items": repo.region_reports()}


@app.post("/v1/voice/report", response_model=VoiceReportResponse)
def report_voice(
    payload: VoiceReportRequest,
    user: Annotated[dict, Depends(require_roles("farmer", "flw", "insurer", "admin"))],
) -> VoiceReportResponse:
    if not is_supported_language(payload.language):
        raise HTTPException(status_code=400, detail="Unsupported language")
    normalized = normalize_transcript(payload.transcript)
    repo.save_voice_report(
        {
            "claim_id": payload.claim_id,
            "language": payload.language.lower(),
            "transcript": payload.transcript,
            "normalized_transcript": normalized,
        }
    )
    write_audit(
        "voice.report_received",
        user["subject"],
        {"claim_id": payload.claim_id, "language": payload.language, "chars": len(payload.transcript)},
    )
    return VoiceReportResponse(
        claim_id=payload.claim_id,
        language=payload.language,
        normalized_transcript=normalized,
    )


@app.get("/v1/voice/languages")
def voice_languages() -> dict:
    return {"items": SUPPORTED_LANGUAGES}


@app.post("/v1/satellite/ndvi", response_model=NdviResponse)
def get_ndvi(
    payload: NdviRequest,
    user: Annotated[dict, Depends(require_roles("flw", "insurer", "admin"))],
) -> NdviResponse:
    ndvi = synthetic_ndvi(payload.latitude, payload.longitude, payload.observation_date)
    write_audit(
        "satellite.ndvi_generated",
        user["subject"],
        {"claim_id": payload.claim_id, "ndvi": ndvi},
    )
    return NdviResponse(claim_id=payload.claim_id, ndvi_value=ndvi, source="sentinel2-sim")


@app.get("/v1/me")
def me(user: Annotated[dict, Depends(get_current_user)]) -> dict:
    return user


@app.get("/v1/ops/latency")
def ops_latency(user: Annotated[dict, Depends(require_roles("admin", "insurer"))]) -> dict:
    return {"items": latency_stats.snapshot()}
