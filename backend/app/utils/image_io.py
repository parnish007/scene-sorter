from io import BytesIO
from typing import List

from fastapi import UploadFile, HTTPException
from PIL import Image

from app.config import settings


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


async def validate_images(files: List[UploadFile]) -> None:
    """
    Validate uploaded images:
    - content type
    - file size
    """
    for f in files:
        if f.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {f.filename} ({f.content_type})"
            )

        # File size check (read without consuming stream)
        contents = await f.read()
        size_mb = len(contents) / (1024 * 1024)

        if size_mb > settings.MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"File '{f.filename}' is too large "
                    f"({size_mb:.2f} MB). "
                    f"Max allowed is {settings.MAX_FILE_SIZE_MB} MB."
                )
            )

        # Reset stream for later reading
        await f.seek(0)


async def read_upload_as_pil_rgb(file: UploadFile) -> Image.Image:
    """
    Read an UploadFile into a PIL Image and convert to RGB.
    """
    try:
        data = await file.read()
        image = Image.open(BytesIO(data))
        image = image.convert("RGB")
        await file.seek(0)
        return image
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image file '{file.filename}': {e}"
        )
