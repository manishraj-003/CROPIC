-- CROPIC-AI Phase 1 schema draft

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    role TEXT NOT NULL CHECK (role IN ('farmer', 'flw', 'insurer', 'admin')),
    phone TEXT UNIQUE,
    full_name TEXT,
    preferred_language TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS farms (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    district TEXT NOT NULL,
    state TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    crop_type TEXT,
    sowing_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS images (
    id UUID PRIMARY KEY,
    farm_id UUID REFERENCES farms(id),
    user_id UUID REFERENCES users(id),
    storage_key TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    captured_at TIMESTAMPTZ NOT NULL,
    blur_score DOUBLE PRECISION,
    tamper_score DOUBLE PRECISION,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS damage_assessments (
    id UUID PRIMARY KEY,
    image_id UUID REFERENCES images(id),
    classifier_label TEXT,
    classifier_confidence DOUBLE PRECISION,
    segmentation_iou DOUBLE PRECISION,
    damage_ratio DOUBLE PRECISION,
    ground_stress_score DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS satellite_records (
    id UUID PRIMARY KEY,
    farm_id UUID REFERENCES farms(id),
    image_id UUID REFERENCES images(id),
    source TEXT DEFAULT 'Sentinel-2',
    ndvi_value DOUBLE PRECISION,
    observation_date DATE,
    raw_payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS claims (
    id UUID PRIMARY KEY,
    farm_id UUID REFERENCES farms(id),
    user_id UUID REFERENCES users(id),
    image_id UUID REFERENCES images(id),
    status TEXT NOT NULL DEFAULT 'submitted',
    discrepancy_score DOUBLE PRECISION,
    fraud_flag BOOLEAN DEFAULT FALSE,
    settlement_amount NUMERIC,
    submitted_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fraud_logs (
    id UUID PRIMARY KEY,
    claim_id UUID REFERENCES claims(id),
    image_id UUID REFERENCES images(id),
    reason TEXT NOT NULL,
    risk_score DOUBLE PRECISION,
    details JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
