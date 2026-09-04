from pydantic import BaseModel
from datetime import datetime
import uuid


class AnalysisCreate(BaseModel):
    code_content: str
    language: str
    file_name: str | None = None
    project_id: uuid.UUID | None = None


class AnalysisResponse(BaseModel):
    id: uuid.UUID
    status: str
    language: str
    file_name: str | None
    overall_score: float | None
    grade: str | None
    scores: dict | None
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisDetailResponse(AnalysisResponse):
    code_content: str
    metadata_: dict | None = None
    report: "ReportResponse | None" = None
    issues: list["IssueResponse"] = []


class AnalysisListResponse(BaseModel):
    items: list[AnalysisResponse]
    total: int
    page: int
    per_page: int
