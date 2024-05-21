from fastapi import APIRouter

from api.routes import predictor
from app.api.routes import upload_review
from app.api.routes import get_review_by_id
from app.api.routes import semantic_query

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
router.include_router(upload_review.router, tags=["upload"], prefix="/v1")
router.include_router(get_review_by_id.router, tags=["get"], prefix="/v1")
router.include_router(semantic_query.router, tags=["semantic query"], prefix="/v1")
