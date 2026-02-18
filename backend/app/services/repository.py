from __future__ import annotations

from datetime import datetime
import sqlite3
import threading
from typing import Any


class Repository:
    def save_metadata(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def create_claim(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def add_audit_flag(self, payload: dict[str, Any]) -> None:
        raise NotImplementedError

    def list_audit_queue(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def summary(self) -> dict[str, Any]:
        raise NotImplementedError

    def clusters(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def region_reports(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def save_voice_report(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class SqliteRepository(Repository):
    def __init__(self, database_url: str) -> None:
        path = database_url.replace("sqlite:///", "", 1)
        self.conn = sqlite3.connect(path, check_same_thread=False, timeout=30)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.Lock()
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA busy_timeout=30000;")
        self._init_schema()

    def _init_schema(self) -> None:
        with self.lock:
            self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS image_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                farm_id TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                captured_at TEXT NOT NULL,
                device_id TEXT NOT NULL,
                blur_score REAL,
                language TEXT,
                district TEXT,
                village TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS claims (
                claim_id TEXT PRIMARY KEY,
                farm_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                image_id TEXT NOT NULL,
                status TEXT NOT NULL,
                discrepancy_score REAL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS audit_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                claim_id TEXT,
                reason TEXT NOT NULL,
                discrepancy REAL,
                ela_score REAL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS voice_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                claim_id TEXT NOT NULL,
                language TEXT NOT NULL,
                transcript TEXT NOT NULL,
                normalized_transcript TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
            )
            self._ensure_column("image_metadata", "district", "TEXT")
            self._ensure_column("image_metadata", "village", "TEXT")
            self.conn.commit()

    def _ensure_column(self, table: str, column: str, column_type: str) -> None:
        rows = self.conn.execute(f"PRAGMA table_info({table})").fetchall()
        existing = {row["name"] for row in rows}
        if column not in existing:
            self.conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")

    def save_metadata(self, payload: dict[str, Any]) -> dict[str, Any]:
        created_at = datetime.utcnow().isoformat()
        with self.lock:
            self.conn.execute(
            """
            INSERT INTO image_metadata
            (user_id, farm_id, latitude, longitude, captured_at, device_id, blur_score, language, district, village, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["user_id"],
                payload["farm_id"],
                payload["latitude"],
                payload["longitude"],
                payload["captured_at"],
                payload["device_id"],
                payload.get("blur_score"),
                payload.get("language"),
                payload.get("district"),
                payload.get("village"),
                created_at,
            ),
            )
            self.conn.commit()
        return {**payload, "created_at": created_at}

    def create_claim(self, payload: dict[str, Any]) -> dict[str, Any]:
        created_at = datetime.utcnow().isoformat()
        record = {**payload, "status": "submitted", "created_at": created_at}
        with self.lock:
            self.conn.execute(
            """
            INSERT OR REPLACE INTO claims
            (claim_id, farm_id, user_id, image_id, status, discrepancy_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["claim_id"],
                payload["farm_id"],
                payload["user_id"],
                payload["image_id"],
                "submitted",
                None,
                created_at,
            ),
            )
            self.conn.commit()
        return record

    def update_claim_discrepancy(self, claim_id: str, discrepancy: float) -> None:
        with self.lock:
            self.conn.execute(
                "UPDATE claims SET discrepancy_score = ? WHERE claim_id = ?",
                (discrepancy, claim_id),
            )
            self.conn.commit()

    def add_audit_flag(self, payload: dict[str, Any]) -> None:
        with self.lock:
            self.conn.execute(
            """
            INSERT INTO audit_queue (claim_id, reason, discrepancy, ela_score, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payload.get("claim_id"),
                payload.get("reason", "manual-review"),
                payload.get("discrepancy"),
                payload.get("ela_score"),
                datetime.utcnow().isoformat(),
            ),
            )
            self.conn.commit()

    def list_audit_queue(self) -> list[dict[str, Any]]:
        with self.lock:
            rows = self.conn.execute(
                "SELECT claim_id, reason, discrepancy, ela_score, created_at FROM audit_queue ORDER BY id DESC LIMIT 200"
            ).fetchall()
        return [dict(row) for row in rows]

    def summary(self) -> dict[str, Any]:
        with self.lock:
            claims_total = self.conn.execute("SELECT COUNT(*) AS c FROM claims").fetchone()["c"]
            pending = self.conn.execute("SELECT COUNT(*) AS c FROM claims WHERE status = 'submitted'").fetchone()["c"]
            avg_damage = self.conn.execute("SELECT AVG(discrepancy_score) AS a FROM claims").fetchone()["a"]
        return {
            "total_claims": claims_total,
            "pending_claims": pending,
            "avg_discrepancy": float(avg_damage) if avg_damage is not None else 0.0,
        }

    def clusters(self) -> list[dict[str, Any]]:
        with self.lock:
            rows = self.conn.execute(
            """
            SELECT ROUND(latitude, 2) AS lat_bin, ROUND(longitude, 2) AS lon_bin, COUNT(*) AS points
            FROM image_metadata
            GROUP BY lat_bin, lon_bin
            ORDER BY points DESC
            LIMIT 100
            """
            ).fetchall()
        return [dict(row) for row in rows]

    def region_reports(self) -> list[dict[str, Any]]:
        with self.lock:
            rows = self.conn.execute(
            """
            SELECT
              COALESCE(m.district, 'unknown') AS district,
              COALESCE(m.village, 'unknown') AS village,
              COUNT(DISTINCT m.id) AS image_reports,
              ROUND(AVG(c.discrepancy_score), 3) AS avg_discrepancy
            FROM image_metadata m
            LEFT JOIN claims c ON c.farm_id = m.farm_id
            GROUP BY district, village
            ORDER BY image_reports DESC
            LIMIT 100
            """
            ).fetchall()
        return [dict(row) for row in rows]

    def save_voice_report(self, payload: dict[str, Any]) -> dict[str, Any]:
        created_at = datetime.utcnow().isoformat()
        with self.lock:
            self.conn.execute(
            """
            INSERT INTO voice_reports (claim_id, language, transcript, normalized_transcript, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payload["claim_id"],
                payload["language"],
                payload["transcript"],
                payload["normalized_transcript"],
                created_at,
            ),
            )
            self.conn.commit()
        return {**payload, "created_at": created_at}


def build_repository(database_url: str) -> Repository:
    if database_url.startswith("sqlite:///"):
        return SqliteRepository(database_url)
    # Fallback: still use local sqlite for development acceleration.
    return SqliteRepository("sqlite:///./cropic_dev.db")
