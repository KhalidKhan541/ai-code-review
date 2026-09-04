from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
import uuid


class Report(BaseModel):
    __tablename__ = "reports"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    recommendations: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    detailed_scores: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    html_content: Mapped[str | None] = mapped_column(Text, nullable=True)

    analysis = relationship("Analysis", back_populates="report")
