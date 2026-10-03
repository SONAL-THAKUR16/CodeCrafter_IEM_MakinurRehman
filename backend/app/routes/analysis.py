import uuid
import logging
from datetime import datetime
from collections import Counter
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.models.analysis import AnalysisRecord
from app.schemas.analysis import (
    AnalyzeRequest,
    AnalyzeResponse,
    AnalyzeResult,
    SentimentAnalysis,
    SentimentScores,
    EmotionScore,
    AcademicSignals,
    AcademicContextFlags,
    PrimaryConcern,
    EvidenceItem,
    HistoryItem,
    HistoryResponse,
    DashboardSummaryResponse,
    DashboardSummaryData,
    DashboardTrendsResponse,
    TrendPoint
)
from app.services.analysis_service import AnalysisService

logger = logging.getLogger("student_analyzer_api")

router = APIRouter(prefix="/api", tags=["Student Feedback Analysis"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze student feedback and persist result",
    description="Analyzes feedback text using context-aware NLP pipeline and stores results in SQLite database."
)
def analyze_feedback(
    payload: AnalyzeRequest,
    db: Session = Depends(get_db)
) -> AnalyzeResponse:
    """
    Route handler for student feedback analysis & persistence.
    Pipeline: Request -> NLP Analysis -> DB Persistence -> Response
    """
    try:
        # Step 1: Run NLP analysis engine
        analysis_result: AnalyzeResult = AnalysisService.analyze_text(payload.text)
        
        # Step 2: Generate unique transaction ID
        analysis_id = f"anl_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        # Step 3: Create database record
        db_record = AnalysisRecord(
            id=analysis_id,
            input_text=payload.text,
            sentiment_label=analysis_result.sentiment.label,
            sentiment_scores=analysis_result.sentiment.scores.model_dump(),
            emotion_results=[e.model_dump() for e in analysis_result.emotions],
            stress_score=analysis_result.signals.stress,
            cognitive_overload_score=analysis_result.signals.cognitive_overload,
            frustration_score=analysis_result.signals.frustration,
            disengagement_score=analysis_result.signals.disengagement,
            workload_difficulty_score=analysis_result.signals.workload_difficulty,
            choice_overload_score=analysis_result.signals.choice_overload,
            time_pressure_score=analysis_result.signals.time_pressure,
            overall_severity=analysis_result.overall_severity,
            severity_reason=analysis_result.severity_reason,
            primary_concern=analysis_result.primary_concern.label,
            primary_concern_score=analysis_result.primary_concern.score,
            evidence=[e.model_dump() for e in analysis_result.evidence],
            explanation=analysis_result.explanation,
            student_insight=analysis_result.student_insight,
            created_at=datetime.now()
        )
        
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return AnalyzeResponse(
            success=True,
            analysis_id=analysis_id,
            analysis=analysis_result
        )
    except SQLAlchemyError as sql_err:
        db.rollback()
        logger.error(f"Database error during feedback persistence: {sql_err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist analysis record in database."
        )
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )
    except Exception as exc:
        logger.error(f"Unexpected error in analyze_feedback: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the feedback analysis."
        )


@router.get(
    "/analyze/{analysis_id}",
    response_model=AnalyzeResponse,
    summary="Retrieve stored feedback analysis",
    description="Fetches a previously saved feedback analysis record from SQLite database by ID."
)
def get_analysis_by_id(
    analysis_id: str,
    db: Session = Depends(get_db)
) -> AnalyzeResponse:
    """Retrieves an individual analysis record by analysis_id."""
    record = db.query(AnalysisRecord).filter(AnalysisRecord.id == analysis_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis record with ID '{analysis_id}' not found."
        )

    # Reconstruct Pydantic result object from database record
    sentiment_dict = record.sentiment_scores or {}
    sentiment_obj = SentimentAnalysis(
        label=record.sentiment_label,
        scores=SentimentScores(
            positive=sentiment_dict.get("positive", 0.0),
            neutral=sentiment_dict.get("neutral", 0.0),
            negative=sentiment_dict.get("negative", 0.0)
        )
    )

    emotions_list = [EmotionScore(**e) for e in (record.emotion_results or [])]
    evidence_list = [EvidenceItem(**e) for e in (record.evidence or [])]

    signals_obj = AcademicSignals(
        stress=record.stress_score,
        cognitive_overload=record.cognitive_overload_score,
        frustration=record.frustration_score,
        disengagement=record.disengagement_score,
        workload_difficulty=record.workload_difficulty_score,
        choice_overload=record.choice_overload_score,
        time_pressure=record.time_pressure_score
    )

    context_flags = AcademicContextFlags(
        workload_pressure=signals_obj.workload_difficulty >= 0.40,
        time_pressure=signals_obj.time_pressure >= 0.40,
        choice_difficulty=signals_obj.choice_overload >= 0.40,
        cognitive_load=signals_obj.cognitive_overload >= 0.40,
        frustration=signals_obj.frustration >= 0.40,
        disengagement=signals_obj.disengagement >= 0.40
    )

    analysis_result = AnalyzeResult(
        sentiment=sentiment_obj,
        emotions=emotions_list,
        signals=signals_obj,
        academic_context=context_flags,
        primary_concern=PrimaryConcern(label=record.primary_concern, score=record.primary_concern_score),
        overall_severity=record.overall_severity,
        severity_reason=record.severity_reason or "",
        evidence=evidence_list,
        explanation=record.explanation,
        student_insight=record.student_insight
    )

    return AnalyzeResponse(
        success=True,
        analysis_id=record.id,
        analysis=analysis_result
    )


@router.get(
    "/history",
    response_model=HistoryResponse,
    summary="Get analysis history",
    description="Retrieves recent student feedback analysis records ordered newest first."
)
def get_analysis_history(
    limit: int = Query(20, ge=1, le=100, description="Maximum number of historical records to return"),
    db: Session = Depends(get_db)
) -> HistoryResponse:
    """Retrieves recent analysis records with text snippets."""
    records = db.query(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).limit(limit).all()
    
    items: List[HistoryItem] = []
    for rec in records:
        snippet = rec.input_text[:60] + "..." if len(rec.input_text) > 60 else rec.input_text
        items.append(
            HistoryItem(
                analysis_id=rec.id,
                created_at=rec.created_at.isoformat() if rec.created_at else datetime.now().isoformat(),
                overall_severity=rec.overall_severity,
                primary_concern=rec.primary_concern,
                stress=rec.stress_score,
                workload_difficulty=rec.workload_difficulty_score,
                text_snippet=snippet
            )
        )

    return HistoryResponse(
        success=True,
        count=len(items),
        items=items,
        history=items
    )


@router.get(
    "/dashboard/summary",
    response_model=DashboardSummaryResponse,
    summary="Get dashboard summary statistics",
    description="Calculates summary statistics across all persisted student analysis records."
)
def get_dashboard_summary(
    db: Session = Depends(get_db)
) -> DashboardSummaryResponse:
    """Calculates real-time statistics from database records."""
    records = db.query(AnalysisRecord).all()
    total = len(records)
    
    if total == 0:
        return DashboardSummaryResponse(
            success=True,
            summary=DashboardSummaryData(
                total_analyses=0,
                average_stress=0.0,
                average_cognitive_overload=0.0,
                average_frustration=0.0,
                average_disengagement=0.0,
                average_workload_difficulty=0.0,
                average_choice_overload=0.0,
                average_time_pressure=0.0,
                severity_distribution={"LOW": 0, "MODERATE": 0, "HIGH": 0},
                most_common_concern="none"
            )
        )

    avg_stress = round(sum(r.stress_score for r in records) / total, 2)
    avg_overload = round(sum(r.cognitive_overload_score for r in records) / total, 2)
    avg_frust = round(sum(r.frustration_score for r in records) / total, 2)
    avg_diseng = round(sum(r.disengagement_score for r in records) / total, 2)
    avg_workload = round(sum(r.workload_difficulty_score for r in records) / total, 2)
    avg_choice = round(sum(r.choice_overload_score for r in records) / total, 2)
    avg_time = round(sum(r.time_pressure_score for r in records) / total, 2)

    severity_counts = Counter(r.overall_severity for r in records)
    severity_dist = {
        "LOW": severity_counts.get("LOW", 0),
        "MODERATE": severity_counts.get("MODERATE", 0),
        "HIGH": severity_counts.get("HIGH", 0)
    }

    # Find most common primary concern
    concerns = [r.primary_concern for r in records if r.primary_concern != "none"]
    most_common = Counter(concerns).most_common(1)[0][0] if concerns else "none"

    return DashboardSummaryResponse(
        success=True,
        summary=DashboardSummaryData(
            total_analyses=total,
            average_stress=avg_stress,
            average_cognitive_overload=avg_overload,
            average_frustration=avg_frust,
            average_disengagement=avg_diseng,
            average_workload_difficulty=avg_workload,
            average_choice_overload=avg_choice,
            average_time_pressure=avg_time,
            severity_distribution=severity_dist,
            most_common_concern=most_common
        )
    )


@router.get(
    "/dashboard/trends",
    response_model=DashboardTrendsResponse,
    summary="Get trend data for charts",
    description="Returns time-series data points for charting student distress and workload trends."
)
def get_dashboard_trends(
    limit: int = Query(20, ge=1, le=100, description="Maximum number of trend data points"),
    db: Session = Depends(get_db)
) -> DashboardTrendsResponse:
    """Fetches recent records and formats them in chronological order for charting."""
    records = db.query(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).limit(limit).all()
    records.reverse()  # Chronological order
    
    trends = [
        TrendPoint(
            analysis_id=r.id,
            created_at=r.created_at.isoformat() if r.created_at else datetime.now().isoformat(),
            stress=r.stress_score,
            cognitive_overload=r.cognitive_overload_score,
            frustration=r.frustration_score,
            workload_difficulty=r.workload_difficulty_score,
            overall_severity=r.overall_severity
        )
        for r in records
    ]

    return DashboardTrendsResponse(
        success=True,
        count=len(trends),
        trends=trends
    )
