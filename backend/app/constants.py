"""
Global constants used across the backend.
Keep ONLY static, non-configurable values here.
(Anything environment-dependent goes into config.py)
"""

# =========================
# SCENE CLASSES
# =========================

SCENE_CLASSES = [
    "buildings",
    "forest",
    "glacier",
    "mountain",
    "sea",
    "street",
]

NUM_CLASSES = len(SCENE_CLASSES)


# =========================
# IMAGE SETTINGS
# =========================

# Allowed MIME types for upload
ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

# Common image extensions
ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


# =========================
# FILE / JOB SETTINGS
# =========================

# Default folder names (used for clarity & consistency)
RAW_DIR_NAME = "raw"
ORGANIZED_DIR_NAME = "organized"
ZIPS_DIR_NAME = "zips"

# Zip naming
ZIP_NAME_PREFIX = "organized_photos"


# =========================
# API METADATA
# =========================

API_TAG_PREDICT = "predict"
API_TAG_BATCH = "batch"
API_TAG_DOWNLOAD = "download"
API_TAG_HEALTH = "health"
