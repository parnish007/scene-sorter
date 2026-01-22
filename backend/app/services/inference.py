import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np
from fastapi import UploadFile, HTTPException

from app.config import settings
from app.services.model_loader import get_model
from app.utils.file_naming import ensure_unique_filename
from app.utils.image_io import read_upload_as_pil_rgb
from app.utils.preprocessing import preprocess_pil_for_model


@dataclass(frozen=True)
class PredictionResult:
    filename: str
    label: str
    confidence: float
    probabilities: List[float]


def _load_class_names() -> List[str]:
    """
    Load class names from labels.json

    Expected format:
    {
      "class_names": ["buildings","forest","glacier","mountain","sea","street"]
    }
    """
    labels_path = settings.labels_path

    if not labels_path.exists():
        raise HTTPException(
            status_code=500,
            detail=f"labels.json not found at: {labels_path}"
        )

    try:
        text = labels_path.read_text(encoding="utf-8").strip()
        if not text:
            raise ValueError("labels.json is empty.")

        payload = json.loads(text)
        class_names = payload.get("class_names", None)

        if not class_names or not isinstance(class_names, list):
            raise ValueError("labels.json must contain key 'class_names' as a list.")

        return [str(x) for x in class_names]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read labels.json: {e}"
        )


def _softmax_np(x: np.ndarray) -> np.ndarray:
    x = x - np.max(x, axis=1, keepdims=True)
    ex = np.exp(x)
    return ex / np.sum(ex, axis=1, keepdims=True)


def _ensure_probabilities(preds: np.ndarray) -> np.ndarray:
    """
    If model returns logits, convert to probabilities.
    If already probabilities, keep as-is.
    """
    preds = np.asarray(preds)

    # Binary edge: (N,) -> (N,2)
    if preds.ndim == 1:
        preds = np.stack([1.0 - preds, preds], axis=1)

    # If not in [0,1] or rows don't sum ~ 1, treat as logits
    row_sums = np.sum(preds, axis=1, keepdims=True)
    looks_like_probs = (
        np.all(preds >= -1e-6) and
        np.all(preds <= 1.0 + 1e-6) and
        np.all(np.abs(row_sums - 1.0) < 1e-2)
    )

    if looks_like_probs:
        return preds

    return _softmax_np(preds)


def _predict_batch(model, batch_array: np.ndarray) -> np.ndarray:
    """
    Returns probabilities of shape (N, num_classes).
    """
    try:
        preds = model.predict(batch_array, verbose=0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {e}")

    preds = np.asarray(preds)
    preds = _ensure_probabilities(preds)
    return preds


def _top1_from_probs(probs: np.ndarray, class_names: List[str]) -> Tuple[str, float, List[float]]:
    idx = int(np.argmax(probs))
    conf = float(probs[idx])

    if idx < len(class_names):
        label = class_names[idx]
    else:
        label = str(idx)

    return label, conf, [float(x) for x in probs.tolist()]


def _apply_mobilenetv2_preprocess(batch: np.ndarray) -> np.ndarray:
    """
    Your preprocess_pil_for_model outputs float32 in [0,1].
    MobileNetV2 preprocess_input expects [0,255] and converts to [-1,1].
    """
    try:
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TensorFlow MobileNetV2 preprocess import failed: {e}")

    batch = batch.astype(np.float32)

    # Convert [0,1] -> [0,255] before preprocess_input
    batch = batch * 255.0

    return preprocess_input(batch)


async def run_batch_inference(files: List[UploadFile], output_dir: Path) -> List[PredictionResult]:
    """
    1) Decode each UploadFile as PIL RGB
    2) Save original image into output_dir (raw)
    3) Preprocess for model input
    4) Predict in a single batch
    5) Return per-image PredictionResult
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    model = get_model()
    class_names = _load_class_names()

    processed: List[np.ndarray] = []
    saved_filenames: List[str] = []

    existing_names: set[str] = set()

    for f in files:
        safe_name = ensure_unique_filename(f.filename or "image.jpg", existing_names)
        save_path = output_dir / safe_name

        pil_img = await read_upload_as_pil_rgb(f)

        try:
            pil_img.save(save_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to save '{safe_name}': {e}")

        # (H,W,3) float32 in [0,1]
        arr = preprocess_pil_for_model(pil_img)
        processed.append(arr)
        saved_filenames.append(safe_name)

    if not processed:
        raise HTTPException(status_code=400, detail="No valid images to process.")

    batch = np.stack(processed, axis=0)  # (N,H,W,3)

    # ✅ Critical fix: make inference preprocessing match MobileNetV2 training
    batch = _apply_mobilenetv2_preprocess(batch)

    probs_batch = _predict_batch(model, batch)

    if probs_batch.ndim != 2:
        raise HTTPException(status_code=500, detail=f"Unexpected model output shape: {probs_batch.shape}")

    if probs_batch.shape[1] != len(class_names):
        raise HTTPException(
            status_code=500,
            detail=(
                f"Class count mismatch: model outputs {probs_batch.shape[1]} classes "
                f"but labels.json has {len(class_names)}."
            )
        )

    results: List[PredictionResult] = []

    for filename, probs in zip(saved_filenames, probs_batch):
        label, conf, probs_list = _top1_from_probs(probs, class_names)
        results.append(
            PredictionResult(
                filename=filename,
                label=label,
                confidence=conf,
                probabilities=probs_list
            )
        )

    return results
