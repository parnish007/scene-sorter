import numpy as np
from PIL import Image

from app.config import settings


def _get_target_size():
    """
    Returns (width, height) from settings.IMAGE_SIZE

    Supports:
    - int (e.g. 224)  -> (224, 224)
    - tuple/list     -> (w, h)
    """
    size = settings.IMAGE_SIZE

    if isinstance(size, (tuple, list)):
        if len(size) != 2:
            raise ValueError("IMAGE_SIZE tuple must be (width, height)")
        target_w, target_h = int(size[0]), int(size[1])
    else:
        s = int(size)
        target_w, target_h = s, s

    return target_w, target_h


def preprocess_pil_for_model(pil_img: Image.Image) -> np.ndarray:
    """
    Converts PIL image to numpy array:
    - RGB
    - resized to target size
    - float32 in range [0,1]

    NOTE: MobileNetV2-specific preprocessing is applied later
          in inference.py (_apply_mobilenetv2_preprocess).
    """
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")

    target_w, target_h = _get_target_size()

    img = pil_img.resize((target_w, target_h))

    arr = np.asarray(img, dtype=np.float32)
    arr = arr / 255.0  # keep [0,1] here

    return arr

