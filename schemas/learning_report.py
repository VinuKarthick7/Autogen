from pydantic import BaseModel

class LearningReport(BaseModel):
    report_id: str
    experiences_processed: int
    experiments_concluded: int
    recommendations_generated: int
    policies_applied: int
