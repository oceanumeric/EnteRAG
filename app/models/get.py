from pydantic import BaseModel


class GetReviewByIdResponse(BaseModel):
    reviews: str