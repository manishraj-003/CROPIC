from app.services.repository import SqliteRepository


def test_sqlite_repository_summary(tmp_path):
    db_path = tmp_path / "test.db"
    repo = SqliteRepository(f"sqlite:///{db_path}")

    repo.create_claim(
        {
            "claim_id": "CLM-1",
            "farm_id": "F1",
            "user_id": "U1",
            "image_id": "I1",
        }
    )
    repo.update_claim_discrepancy("CLM-1", 0.4)
    summary = repo.summary()
    assert summary["total_claims"] == 1
    assert summary["pending_claims"] == 1
    assert abs(summary["avg_discrepancy"] - 0.4) < 1e-9


def test_region_reports(tmp_path):
    db_path = tmp_path / "test_regions.db"
    repo = SqliteRepository(f"sqlite:///{db_path}")
    repo.save_metadata(
        {
            "user_id": "U1",
            "farm_id": "F1",
            "latitude": 10.0,
            "longitude": 11.0,
            "captured_at": "2026-01-01T10:00:00Z",
            "device_id": "D1",
            "district": "karnal",
            "village": "v1",
        }
    )
    reports = repo.region_reports()
    assert reports
    assert reports[0]["district"] == "karnal"
