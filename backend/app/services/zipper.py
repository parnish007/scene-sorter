from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from fastapi import HTTPException

from app.utils.temp_storage import get_job_dirs


def zip_folder(source_dir: Path, job_id: str) -> Path:
    """
    Zip the organized folder for a given job_id.

    - source_dir: typically .../{job_id}/organized
    - output: .../{job_id}/zips/organized_photos_{job_id}.zip

    Returns:
      Path to the created zip file.
    """
    if not source_dir.exists() or not source_dir.is_dir():
        raise HTTPException(
            status_code=500,
            detail=f"Source directory not found for zipping: {source_dir}"
        )

    job_dirs = get_job_dirs(job_id)
    zips_dir = job_dirs["zips"]
    zips_dir.mkdir(parents=True, exist_ok=True)

    zip_path = zips_dir / f"organized_photos_{job_id}.zip"

    # If zip already exists, overwrite it
    if zip_path.exists():
        try:
            zip_path.unlink()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to overwrite existing zip: {zip_path} ({e})"
            )

    try:
        with ZipFile(zip_path, mode="w", compression=ZIP_DEFLATED) as zf:
            # Walk all files and write them with relative paths
            for file_path in source_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(source_dir)  # keep folder structure
                    zf.write(file_path, arcname.as_posix())

        return zip_path

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create zip for job '{job_id}': {e}"
        )
