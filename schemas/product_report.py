from pydantic import BaseModel

class ProductReport(BaseModel):
    report_id: str
    product_name: str
    requirements_count: int
    epics_count: int
    stories_count: int
    total_estimated_points: int
