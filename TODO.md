# CROPIC-AI Execution Roadmap (Hackathon Edition)

## Phase 1: Foundation and Data Acquisition (Weeks 1–3)
**Goal:** Establishing the "Ground Truth".
- [ ] **Infrastructure Setup**
    - [ ] Initialize Monorepo (Git, Docker, etc.)
    - [ ] **Backend:** FastAPI (Python) setup
    - [ ] **Database:** Supabase/PostgreSQL configuration
- [ ] **Data Aggregation**
    - [ ] **Image Datasets:** Scraper scripts for PlantVillage, DLCPD-25 (Target: ~50k images)
    - [ ] **Satellite:** Google Earth Engine (GEE) Sentinel-2 integration scripts
- [ ] **User Research**
    - [ ] Define User Personas & Constraints (FLWs, Farmers)

## Phase 2: Core Development - The "MVP" (Weeks 4–7)
**Goal:** Capture-to-Dashboard Pipeline.
- [ ] **Mobile App (React Native)**
    - [ ] "Ghost Overlay" UI for standardized capture
    - [ ] Edge-AI Validation (Laplacian blur detection)
- [ ] **Cloud AI**
    - [ ] Deploy MobileNetV2/ResNet-50 (>85% accuracy)
    - [ ] API for crop type/growth stage
- [ ] **Authority Dashboard (ReactJS)**
    - [ ] Map-based visualization of stress clusters

## Phase 3: Intelligence & Verification (Weeks 8–11)
**Goal:** Technical Depth.
- [ ] **Damage Segmentation Engine**
    - [ ] U-Net/DeepLabV3+ implementation
    - [ ] Damage ratio calculation
- [ ] **Dual-Verification Engine**
    - [ ] NDVI vs Ground Image Stress Logic
    - [ ] Discrepancy flagging ($\delta > 0.3$)
- [ ] **Inclusivity**
    - [ ] Bhashini WebSocket API integration (Voice)

## Phase 4: Grand Finale Sprint
**Goal:** Market Readiness & Polish.
- [ ] **Anti-Tamper Layer**
    - [ ] Error Level Analysis (ELA) implementation
- [ ] **Optimization**
    - [ ] TensorRT / Fog Computing setup (<2s inference)
- [ ] **Final Polish**
    - [ ] "Field Reality" UI palettes
    - [ ] TRL Roadmap creation
