from fastapi import FastAPI
from app.api import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="EssayGenie",
        description="EssayGenie————基于大模型的智能作文教学体",
        version="0.1.0",
    )
    
    app.include_router(api_router, prefix="/api")
    return app


app = create_app()