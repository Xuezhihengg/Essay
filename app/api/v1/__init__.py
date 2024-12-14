from .eec import eec_router
from fastapi import APIRouter


v1_router = APIRouter()

v1_router.include_router(eec_router, prefix="/eec")