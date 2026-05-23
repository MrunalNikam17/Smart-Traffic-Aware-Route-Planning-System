import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_path: Path = Path(__file__).resolve().parents[1] / "ml" / "Optimized_Traffic_Model.pkl"
    scaler_path: Path = Path(__file__).resolve().parents[1] / "ml" / "Traffic_Scaler.pkl"
    api_prefix: str = "/api"
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
