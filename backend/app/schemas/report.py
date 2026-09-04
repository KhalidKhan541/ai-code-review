from pydantic import BaseModel
from datetime import datetime
import uuid


class ReportResponse(BaseModel):
    id: uuid.UUID
    summary: str
    recommendations: dict | None
    detailed_scores: dict | None
    created_at: datetime

    class Config:
        from_attributes = True


class IssueResponse(BaseModel):
    id: uuid.UUID
    category: str
    severity: str
    line_number: int | None
    column: int | None
    message: str
    suggestion: str | None
    rule_id: str | None

    class Config:
        from_attributes = True
