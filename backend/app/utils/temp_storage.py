import shutil
from pathlib import Path
from typing import Dict

from fastapi import HTTPException

from app.config import settings


def create_job_dirs(job_id: str) -> Dict[str, Path]:
    """
    Creates an isolated workspace for a single batch upload job.

    Structure:
      TEMP_ROOT/
        {job_id}/
          raw/        -> original uploaded images saved here
          organized/  -> images sorted into class folders here
          zips/       -> generated zip file stored here

    Returns dict with paths.
    """
    temp_root = settings.temp_root
    job_root = temp_root / job_id

    raw_dir = job_root / "raw"
    organized_dir = job_root / "organized"
    zips_dir = job_root / "zips"

    try:
        raw_dir.mkdir(parents=True, exist_ok=True)
        organized_dir.mkdir(parents=True, exist_ok=True)
        zips_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create temp directories for job '{job_id}': {e}"
        )

    return {
        "root": job_root,
        "raw": raw_dir,
        "organized": organized_dir,
        "zips": zips_dir,
    }


def get_job_dirs(job_id: str) -> Dict[str, Path]:
    """
    Get workspace directories for an existing job_id.
    Raises if job does not exist.
    """
    temp_root = settings.temp_root
    job_root = temp_root / job_id

    raw_dir = job_root / "raw"
    organized_dir = job_root / "organized"
    zips_dir = job_root / "zips"

    if not job_root.exists():
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")

    return {
        "root": job_root,
        "raw": raw_dir,
        "organized": organized_dir,
        "zips": zips_dir,
    }


def cleanup_job(job_id: str) -> None:
    """
    Delete all files/folders for a job_id to free space.
    """
    temp_root = settings.temp_root
    job_root = temp_root / job_id

    if not job_root.exists():
        return

    try:
        shutil.rmtree(job_root)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cleanup job '{job_id}': {e}"
        )
