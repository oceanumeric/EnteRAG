from pydantic import BaseModel


class UploadReviewResponse(BaseModel):
    document_id: str
