import re
from pathlib import Path


def make_safe_filename(filename: str) -> str:
    """
    Convert an incoming filename into a safe filename.

    - Removes path parts (prevents ../../ attacks)
    - Keeps extension if present
    - Replaces unsafe characters
    - Ensures non-empty name
    """

    # Remove any directory parts (Windows/Linux)
    name = Path(filename).name

    # Split name and extension
    stem = Path(name).stem
    suffix = Path(name).suffix.lower()

    # Clean stem: allow letters, numbers, dash, underscore
    cleaned_stem = re.sub(r"[^a-zA-Z0-9_-]+", "_", stem).strip("_")

    if not cleaned_stem:
        cleaned_stem = "image"

    # Keep common extensions only; if unknown, default to .jpg
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        suffix = ".jpg"

    return f"{cleaned_stem}{suffix}"


def ensure_unique_filename(filename: str, existing_names: set[str]) -> str:
    """
    If filename already exists in existing_names, append _1, _2, etc.
    """
    safe = make_safe_filename(filename)

    if safe not in existing_names:
        existing_names.add(safe)
        return safe

    stem = Path(safe).stem
    suffix = Path(safe).suffix

    i = 1
    while True:
        candidate = f"{stem}_{i}{suffix}"
        if candidate not in existing_names:
            existing_names.add(candidate)
            return candidate
        i += 1
