import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name, "").strip().lower()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    # API meta
    API_TITLE: str = "Scene Sorter API"
    API_VERSION: str = "1.0.0"

    # Runtime flags
    DEBUG: bool = _env_bool("SCENE_SORTER_DEBUG", False)

    # Batch limits
    MAX_FILES_PER_BATCH: int = _env_int("SCENE_SORTER_MAX_FILES_PER_BATCH", 50)
    MAX_FILE_SIZE_MB: int = _env_int("SCENE_SORTER_MAX_FILE_SIZE_MB", 10)

    # Image preprocessing (must match training)
    IMAGE_SIZE: Tuple[int, int] = (224, 224)

    # CORS
    @property
    def CORS_ALLOW_ORIGINS(self) -> List[str]:
        raw = os.getenv("SCENE_SORTER_CORS_ALLOW_ORIGINS", "http://localhost:3000")
        return [x.strip() for x in raw.split(",") if x.strip()]

    # Repo root
    @property
    def repo_root(self) -> Path:
        # backend/app/config.py → repo root
        return Path(__file__).resolve().parents[2]

    # Model paths
    @property
    def model_path(self) -> Path:
        env = os.getenv("SCENE_SORTER_MODEL_PATH")
        if env:
            return Path(env).expanduser().resolve()
        return (self.repo_root / "model" / "exported" / "best_finetuned_model.keras")

    @property
    def labels_path(self) -> Path:
        env = os.getenv("SCENE_SORTER_LABELS_PATH")
        if env:
            return Path(env).expanduser().resolve()
        return (self.repo_root / "model" / "exported" / "labels.json")

    # Temp storage (repo root, git-ignored)
    @property
    def temp_root(self) -> Path:
        env = os.getenv("SCENE_SORTER_TEMP_ROOT")
        if env:
            return Path(env).expanduser().resolve()
        return self.repo_root / ".scene_sorter_tmp"


settings = Settings()
