from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.models.report import Report
from app.models.issue import Issue
from app.schemas.analysis import AnalysisCreate, AnalysisResponse, AnalysisDetailResponse, AnalysisListResponse
from app.api.deps import get_current_user_dependency
from app.services.ai_engine import AIEngine

router = APIRouter(prefix="/analysis", tags=["Code Analysis"])

ai_engine = AIEngine()


@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    data: AnalysisCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency),
):
    analysis = Analysis(
        user_id=current_user.id,
        code_content=data.code_content,
        language=data.language,
        file_name=data.file_name,
        project_id=data.project_id,
        status="processing",
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)

    try:
        result = await ai_engine.analyze_code(data.code_content, data.language)

        analysis.status = "completed"
        analysis.overall_score = result["overall_score"]
        analysis.grade = result["grade"]
        analysis.scores = result["scores"]
        analysis.metadata_ = result.get("metadata")

        report = Report(
            analysis_id=analysis.id,
            summary=result["summary"],
            recommendations=result.get("recommendations"),
            detailed_scores=result.get("detailed_scores"),
        )
        db.add(report)

        for issue_data in result.get("issues", []):
            issue = Issue(analysis_id=analysis.id, **issue_data)
            db.add(issue)

        await db.commit()
        await db.refresh(analysis)

    except Exception:
        analysis.status = "failed"
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis failed. Please try again.",
        )

    return analysis


@router.get("/", response_model=AnalysisListResponse)
async def list_analyses(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency),
):
    query = select(Analysis).where(Analysis.user_id == current_user.id)
    count_query = select(func.count()).select_from(Analysis).where(Analysis.user_id == current_user.id)

    total = (await db.execute(count_query)).scalar()
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    analyses = result.scalars().all()

    return AnalysisListResponse(
        items=analyses,
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/{analysis_id}", response_model=AnalysisDetailResponse)
async def get_analysis(
    analysis_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency),
):
    result = await db.execute(
        select(Analysis).where(
            Analysis.id == analysis_id,
            Analysis.user_id == current_user.id,
        )
    )
    analysis = result.scalar_one_or_none()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )

    report_result = await db.execute(select(Report).where(Report.analysis_id == analysis.id))
    report = report_result.scalar_one_or_none()

    issues_result = await db.execute(select(Issue).where(Issue.analysis_id == analysis.id))
    issues = issues_result.scalars().all()

    return AnalysisDetailResponse(
        **analysis.__dict__,
        report=report,
        issues=issues,
    )
