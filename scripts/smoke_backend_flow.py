import requests

BASE = "http://127.0.0.1:8000"


def post(path: str, payload: dict, token: str | None = None) -> dict:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.post(f"{BASE}{path}", json=payload, headers=headers, timeout=5)
    r.raise_for_status()
    return r.json()


def get(path: str, token: str | None = None) -> dict:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(f"{BASE}{path}", headers=headers, timeout=5)
    r.raise_for_status()
    return r.json()


def main() -> None:
    insurer_token = post("/v1/auth/token", {"phone": "9999999999", "role": "insurer"})["access_token"]
    flw_token = post("/v1/auth/token", {"phone": "8888888888", "role": "flw"})["access_token"]

    post(
        "/v1/images/metadata",
        {
            "user_id": "U1",
            "farm_id": "FARM-1",
            "latitude": 23.12,
            "longitude": 77.42,
            "captured_at": "2026-02-18T10:00:00Z",
            "device_id": "DEV-1",
            "blur_score": 18.3,
            "language": "hi",
            "district": "karnal",
            "village": "sample-village",
        },
        flw_token,
    )
    post("/v1/claims", {"claim_id": "CLM-1", "farm_id": "FARM-1", "user_id": "U1", "image_id": "IMG-1"}, flw_token)
    post("/v1/ai/classify", {"image_id": "IMG-1"}, flw_token)
    post("/v1/ai/segment", {"image_id": "IMG-1", "healthy_pixels": 80, "damaged_pixels": 20}, flw_token)
    stress = post("/v1/ai/stress", {"claim_id": "CLM-1", "damage_ratio": 0.45, "ndvi_hint": 0.2}, flw_token)
    post(
        "/v1/verification/dual",
        {"claim_id": "CLM-1", "ground_stress": stress["ground_stress"], "satellite_ndvi": 0.1},
        insurer_token,
    )
    post("/v1/voice/report", {"claim_id": "CLM-1", "language": "hi", "transcript": "crop damaged by rain"}, flw_token)
    summary = get("/v1/dashboard/summary", insurer_token)
    queue = get("/v1/audit/queue", insurer_token)
    clusters = get("/v1/dashboard/clusters", insurer_token)
    regions = get("/v1/dashboard/regions", insurer_token)

    print("summary:", summary)
    print("audit_count:", len(queue.get("items", [])))
    print("cluster_count:", len(clusters.get("items", [])))
    print("region_count:", len(regions.get("items", [])))


if __name__ == "__main__":
    main()
