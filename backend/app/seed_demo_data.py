import os
import sys
import uuid
import logging
from datetime import datetime, timedelta

# Ensure backend folder is on python path when running script directly
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database import SessionLocal, init_db
from app.models.analysis import AnalysisRecord
from app.services.analysis_service import AnalysisService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed_demo_data")

DEMO_STUDENT_FEEDBACKS = [
    "I am enjoying this course and I feel confident about my assignments.",
    "I have four assignments due this week and I don't know which one to complete first.",
    "The course is fine, but the number of assignments is becoming frustrating.",
    "I am not stressed about the upcoming exam.",
    "I am extremely overwhelmed. I cannot concentrate and I feel like I have too much work.",
    "I don't have any problems with the workload.",
    "I have three assignments due tomorrow and I cannot concentrate.",
    "I am slightly worried about one assignment.",
    "I stopped participating because I lost interest in the lectures.",
    "The coursework is heavy, but I am learning a lot and managing my time."
]


def seed_demo_data():
    """Seeds database with fictional anonymized student feedback records for dashboard testing."""
    logger.info("Initializing database tables for demo seeding...")
    init_db()
    
    db = SessionLocal()
    try:
        existing_count = db.query(AnalysisRecord).count()
        logger.info(f"Current database record count: {existing_count}")
        
        created_count = 0
        base_time = datetime.utcnow() - timedelta(days=5)

        for idx, text in enumerate(DEMO_STUDENT_FEEDBACKS):
            analysis_result = AnalysisService.analyze_text(text)
            
            # Spread timestamps over past 5 days for trend visualization
            created_time = base_time + timedelta(hours=idx * 12)
            analysis_id = f"anl_{created_time.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
            
            record = AnalysisRecord(
                id=analysis_id,
                input_text=text,
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
                created_at=created_time
            )
            db.add(record)
            created_count += 1

        db.commit()
        logger.info(f"Successfully seeded {created_count} fictional anonymized student feedback records into SQLite database.")
    except Exception as exc:
        db.rollback()
        logger.error(f"Error seeding demo data: {exc}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
