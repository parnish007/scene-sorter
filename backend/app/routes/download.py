from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.utils.temp_storage import get_job_dirs

router = APIRouter(prefix="/download", tags=["download"])


@router.get("/{job_id}")
def download_zip(job_id: str):
    """
    Download the organized zip for a job_id.

    Expects zip at:
      TEMP_ROOT/{job_id}/zips/organized_photos_{job_id}.zip
    """
    job_dirs = get_job_dirs(job_id)
    zips_dir: Path = job_dirs["zips"]

    zip_path = zips_dir / f"organized_photos_{job_id}.zip"

    if not zip_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Zip not found. Run /predict/batch first to generate it."
        )

    return FileResponse(
        path=str(zip_path),
        filename=zip_path.name,
        media_type="application/zip",
    )
