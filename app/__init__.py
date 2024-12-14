from fastapi import FastAPI
import logging.config
from app.api import api_router
from app.settings import settings

logging.config.dictConfig(settings.LOGGING_CONFIG)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.VERSION,
    )
    
    app.include_router(api_router, prefix="/api")
    return app


app = create_app()