from fastapi import FastAPI

from app.config import settings
from app.middleware.cors import setup_cors

from app.routes.health import router as health_router
from app.routes.predict import router as predict_router
from app.routes.batch import router as batch_router
from app.routes.download import router as download_router

from app.services.model_loader import get_model
from app.routes.predict import router as predict_router



def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
    )

    # Middleware
    setup_cors(app)

    # Routes
    app.include_router(health_router)
    app.include_router(predict_router)
    app.include_router(batch_router)
    app.include_router(download_router)

    # Optional: warm up model at startup (faster first request)
    @app.on_event("startup")
    def _startup() -> None:
        get_model()

    return app


app = create_app()
