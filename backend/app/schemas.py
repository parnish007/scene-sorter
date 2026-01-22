from typing import Dict, List
from typing_extensions import TypedDict

from pydantic import BaseModel, Field


class ImagePrediction(BaseModel):
    filename: str = Field(..., description="Saved filename of the image on the server")
    label: str = Field(..., description="Predicted scene label (top-1)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for top-1 label")


class BatchSummary(TypedDict):
    total: int
    by_class: Dict[str, int]


class BatchPredictResponse(BaseModel):
    job_id: str = Field(..., description="Unique job id for this batch upload")
    summary: BatchSummary = Field(..., description="Summary counts for the batch")
    results: List[ImagePrediction] = Field(..., description="Per-image top-1 predictions")
    download_url: str = Field(..., description="Relative URL to download the organized zip")
