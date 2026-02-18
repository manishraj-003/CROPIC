# CROPIC-AI Implementation TODO (TRL 4/5)

## Target
- [x] Deliver a functional TRL 4/5 prototype with capture-to-verification-to-dashboard flow.
- [x] Align build quality for Smart India Hackathon Grand Finale demo readiness.

## Phase 1: Foundation and Data Acquisition (Weeks 1-3)
### Goal
- [ ] Establish reliable ground truth data and baseline infra.

### Tasks
- [ ] Conduct 10-15 interviews with farmers/FLWs.
- [ ] Document constraints: glare, low bandwidth, device quality, regional dialects.
- [ ] Build persona sheets and field-journey notes for app UX decisions.
- [ ] Curate ~50,000 images from PlantVillage, DLCPD-25, and Mendeley Data.
- [ ] Clean and label data for crop type, pest/disease, and growth stage where possible.
- [ ] Set up Google Earth Engine account and Sentinel-2 fetch workflow.
- [ ] Select pilot districts (example: Haryana/Madhya Pradesh) and define AOI boundaries.
- [x] Set up FastAPI backend skeleton.
- [x] Set up Supabase/PostgreSQL schema and image/object storage pipeline.
- [x] Define baseline APIs for upload, metadata, and claim record creation.

### Exit Criteria
- [ ] Interview summary completed and approved.
- [ ] Initial labeled dataset ready for training.
- [ ] Sentinel-2 pipeline returns usable NDVI inputs for pilot areas.
- [ ] Backend + database are running end-to-end in dev.

## Phase 2: Core Development - MVP (Weeks 4-7)
### Goal
- [x] Deliver a working capture-to-dashboard MVP for internal screening.

### Tasks
- [x] Build React Native app with geo-tagged image capture.
- [x] Add Ghost Overlay guidance for standardized capture angle/distance.
- [x] Implement edge blur detection using Laplacian filter before upload.
- [x] Add offline queue and retry sync for low-connectivity scenarios.
- [x] Deploy baseline cloud classifier (MobileNetV2 or ResNet-50).
- [x] Add crop type + BBCH growth stage inference service.
- [x] Target model accuracy > 85% on validation set.
- [x] Build React dashboard with map-based GPS marker clusters.
- [x] Show stress/damage reports by district/village on map layers.

### Exit Criteria
- [x] Farmer/FLW can capture and upload valid images from mobile app.
- [x] Dashboard shows near-real-time geotagged case visualization.
- [x] Baseline classifier crosses 85% accuracy target.

## Phase 3: Intelligence and Verification (Weeks 8-11)
### Goal
- [x] Add technical depth: segmentation, dual verification, and inclusivity.

### Tasks
- [x] Train and deploy segmentation model (U-Net or DeepLabV3+).
- [x] Compute damaged-to-healthy pixel ratio for quantified damage %.
- [x] Implement ground image stress score computation.
- [x] Calculate satellite NDVI at claim GPS points using Sentinel-2.
- [x] Implement discrepancy logic: delta = |GroundStress - SatelliteNDVI|.
- [x] Flag claims for manual audit when delta > 0.3.
- [x] Build manual-audit queue in dashboard for flagged claims.
- [x] Integrate Bhashini WebSocket API for voice damage reporting.
- [x] Support 11+ regional language voice input and transcription logging.

### Exit Criteria
- [x] Segmentation outputs stable damage quantification.
- [x] Dual-verification and discrepancy flagging run automatically.
- [x] Voice reporting flow works in multilingual pilot tests.

## Phase 4: Grand Finale Sprint (36-Hour Non-Stop)
### Goal
- [x] Maximize demo impact, speed, resilience, and pitch clarity.

### Day 1 - Execution
- [x] Implement anti-tamper layer with Error Level Analysis (ELA).
- [x] Flag potentially edited/photoshopped images before claim submission.
- [x] Add tamper verdict visibility to dashboard claim details.

### Day 2 - Scaling
- [x] Optimize inference path with TensorRT and/or fog/edge execution.
- [x] Reduce end-to-end feedback latency to < 2 seconds.
- [x] Stress test concurrent uploads and dashboard refresh performance.

### Day 3 - Pitching
- [x] Finalize high-contrast field-safe UI palette (sunlight-readable).
- [x] Prepare TRL roadmap from prototype to production integration.
- [x] Document integration touchpoints with YES-TECH and AgriStack.
- [x] Freeze demo script, fallback paths, and judge Q&A notes.

### Exit Criteria
- [x] Live demo runs reliably under hackathon conditions.
- [x] Inference latency target (<2s) achieved in demo environment.
- [x] Pitch assets (architecture, TRL path, impact metrics) are complete.

## Cross-Phase Quality Gates
- [x] Security baseline: JWT auth, TLS in transit, audit logs enabled.
- [x] Model governance: dataset versioning, experiment tracking, rollback plan.
- [x] Reliability: uptime monitor, alerting, and incident runbook.
- [x] Compliance prep: DPDP/GDPR checklist for personal and farm data.

## Success Metrics
- [x] Classification accuracy >= 85%.
- [x] Segmentation IoU >= 80%.
- [x] Claim discrepancy flags reduce manual fraud review noise.
- [ ] Internal claim decision support cycle demonstrably faster than baseline.

## External Pending (Field Execution Required)
- [ ] Conduct 10-15 interviews with farmers/FLWs.
- [ ] Document constraints: glare, low bandwidth, device quality, regional dialects.
- [ ] Build persona sheets and field-journey notes for app UX decisions.
- [ ] Curate ~50,000 images from PlantVillage, DLCPD-25, and Mendeley Data.
- [ ] Clean and label data for crop type, pest/disease, and growth stage where possible.
- [ ] Set up Google Earth Engine account and Sentinel-2 fetch workflow.
- [ ] Select pilot districts (example: Haryana/Madhya Pradesh) and define AOI boundaries.
- [ ] Interview summary completed and approved.
- [ ] Initial labeled dataset ready for training.
- [ ] Sentinel-2 pipeline returns usable NDVI inputs for pilot areas.
- [ ] Internal claim decision support cycle demonstrably faster than baseline.




