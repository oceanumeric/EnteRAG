from fastapi import APIRouter

from api.routes import predictor
from api.routes import upload

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
router.include_router(upload.router, tags=["upload"], prefix="/v1")
