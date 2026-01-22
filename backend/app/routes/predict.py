from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas import ImagePrediction
from app.services.inference import run_batch_inference
from app.utils.image_io import validate_images
from app.utils.temp_storage import create_job_dirs


router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("", response_model=ImagePrediction)
async def predict_single(file: UploadFile = File(...)):
    """
    Predict scene class for a single image.
    Useful for quick testing and demos.
    """

    # Reuse batch validation logic
    await validate_images([file])

    # Create a lightweight job workspace
    job_id = "single"
    job_dirs = create_job_dirs(job_id)

    # Run inference using batch pipeline (with 1 image)
    predictions = await run_batch_inference(
        files=[file],
        output_dir=job_dirs["raw"]
    )

    if not predictions:
        raise HTTPException(status_code=500, detail="Prediction failed.")

    pred = predictions[0]

    return ImagePrediction(
        filename=pred.filename,
        label=pred.label,
        confidence=pred.confidence
    )
