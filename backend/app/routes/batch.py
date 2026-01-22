from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from uuid import uuid4

from app.config import settings
from app.schemas import BatchPredictResponse, ImagePrediction
from app.services.inference import run_batch_inference
from app.services.organizer import organize_images
from app.services.zipper import zip_folder
from app.utils.image_io import validate_images
from app.utils.temp_storage import create_job_dirs

router = APIRouter(prefix="/predict", tags=["batch"])


@router.post("/batch", response_model=BatchPredictResponse)
async def batch_predict(files: List[UploadFile] = File(...)):
    """
    Accept multiple images, run scene classification,
    organize them into class-based folders, zip the result,
    and return a download URL.
    """

    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    if len(files) > settings.MAX_FILES_PER_BATCH:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {settings.MAX_FILES_PER_BATCH} files allowed per batch."
        )

    # Validate file types & sizes
    await validate_images(files)

    # Create unique job workspace
    job_id = uuid4().hex
    job_dirs = create_job_dirs(job_id)

    # Run inference
    predictions = await run_batch_inference(
        files=files,
        output_dir=job_dirs["raw"]
    )

    # Organize images into folders by class
    organize_images(
        predictions=predictions,
        raw_dir=job_dirs["raw"],
        organized_dir=job_dirs["organized"]
    )

    # Zip organized folder
    zip_path = zip_folder(
        source_dir=job_dirs["organized"],
        job_id=job_id
    )

    # Build response
    by_class = {}
    results = []

    for pred in predictions:
        by_class[pred.label] = by_class.get(pred.label, 0) + 1
        results.append(
            ImagePrediction(
                filename=pred.filename,
                label=pred.label,
                confidence=pred.confidence
            )
        )

    return BatchPredictResponse(
        job_id=job_id,
        summary={
            "total": len(predictions),
            "by_class": by_class
        },
        results=results,
        download_url=f"/download/{job_id}"
    )
