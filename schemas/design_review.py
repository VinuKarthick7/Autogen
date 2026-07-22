from pydantic import BaseModel

class DesignReview(BaseModel):
    review_id: str
    rfc_id: str
    reviewer_id: str
    comments: str
    approved: bool

