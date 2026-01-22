from pathlib import Path
from typing import Optional

import tensorflow as tf
from fastapi import HTTPException

from app.config import settings

# Global singleton (loaded once)
_MODEL: Optional[tf.keras.Model] = None


def _load_model_from_disk(model_path: Path) -> tf.keras.Model:
    """
    Load a Keras model from disk with safe defaults.
    """
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load model from '{model_path}': {e}"
        )


def get_model() -> tf.keras.Model:
    """
    Returns a singleton Keras model instance.
    Loads the model only once during app lifetime.
    """
    global _MODEL

    if _MODEL is not None:
        return _MODEL

    model_path = settings.model_path

    if not model_path.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Model file not found at: {model_path}"
        )

    _MODEL = _load_model_from_disk(model_path)
    return _MODEL
