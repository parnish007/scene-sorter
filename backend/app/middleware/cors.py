from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.config import settings


def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the FastAPI application.

    This allows the frontend (Next.js / React) to communicate
    with the backend API safely.
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.CORS_ALLOW_ORIGINS),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
