import shutil
from pathlib import Path
from typing import Iterable

from fastapi import HTTPException


def _safe_folder_name(name: str) -> str:
    """
    Keep folder names predictable and filesystem-safe.
    """
    name = (name or "").strip().lower()
    if not name:
        return "unknown"
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in name)


def organize_images(
    predictions: Iterable,
    raw_dir: Path,
    organized_dir: Path,
    copy_files: bool = True,
) -> None:
    """
    Organize images into class folders.

    Inputs:
    - predictions: iterable of objects with attributes:
        - filename (str)
        - label (str)
    - raw_dir: folder containing the saved raw images
    - organized_dir: folder where class subfolders will be created
    - copy_files: if True -> copy images, else -> move images

    Output:
    organized_dir/
      buildings/
      forest/
      glacier/
      mountain/
      sea/
      street/
    """
    if not raw_dir.exists():
        raise HTTPException(status_code=500, detail=f"raw_dir not found: {raw_dir}")

    organized_dir.mkdir(parents=True, exist_ok=True)

    op = shutil.copy2 if copy_files else shutil.move

    for pred in predictions:
        filename = getattr(pred, "filename", None)
        label = getattr(pred, "label", None)

        if not filename or not label:
            raise HTTPException(
                status_code=500,
                detail="Invalid prediction object: missing 'filename' or 'label'."
            )

        src_path = raw_dir / filename
        if not src_path.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Predicted file not found in raw_dir: {src_path}"
            )

        folder_name = _safe_folder_name(label)
        dest_folder = organized_dir / folder_name
        dest_folder.mkdir(parents=True, exist_ok=True)

        dest_path = dest_folder / filename

        try:
            op(src_path, dest_path)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to organize '{filename}' into '{folder_name}': {e}"
            )
