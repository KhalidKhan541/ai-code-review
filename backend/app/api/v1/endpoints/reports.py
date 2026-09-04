from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.models.report import Report
from app.models.issue import Issue
from app.schemas.report import ReportResponse, IssueResponse
from app.api.deps import get_current_user_dependency

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/{analysis_id}", response_model=ReportResponse)
async def get_report(
    analysis_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency),
):
    analysis_result = await db.execute(
        select(Analysis).where(
            Analysis.id == analysis_id,
            Analysis.user_id == current_user.id,
        )
    )
    analysis = analysis_result.scalar_one_or_none()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )

    report_result = await db.execute(select(Report).where(Report.analysis_id == analysis.id))
    report = report_result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    return report


@router.get("/{analysis_id}/issues", response_model=list[IssueResponse])
async def get_analysis_issues(
    analysis_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency),
):
    analysis_result = await db.execute(
        select(Analysis).where(
            Analysis.id == analysis_id,
            Analysis.user_id == current_user.id,
        )
    )
    analysis = analysis_result.scalar_one_or_none()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )

    issues_result = await db.execute(select(Issue).where(Issue.analysis_id == analysis.id))
    return issues_result.scalars().all()
