from dataclasses import dataclass
import os


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "CROPIC-AI Backend")
    env: str = os.getenv("ENV", "dev")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./cropic_dev.db")
    discrepancy_threshold: float = float(os.getenv("DISCREPANCY_THRESHOLD", "0.3"))
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-only-change-in-prod")


settings = Settings()
