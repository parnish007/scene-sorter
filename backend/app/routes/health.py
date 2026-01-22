from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {
        "status": "ok",
        "message": "Scene Sorter API is running"
    }
