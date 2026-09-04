from sqlalchemy import String, Text, ForeignKey, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
import uuid


class Analysis(BaseModel):
    __tablename__ = "analyses"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    code_content: Mapped[str] = mapped_column(Text, nullable=False)
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    grade: Mapped[str | None] = mapped_column(String(5), nullable=True)
    scores: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)

    user = relationship("User", back_populates="analyses")
    project = relationship("Project", back_populates="analyses")
    report = relationship("Report", back_populates="analysis", uselist=False)
    issues = relationship("Issue", back_populates="analysis")
