from datetime import datetime
from sqlalchemy import Column, String, Float, Text, JSON, DateTime
from app.database import Base


class AnalysisRecord(Base):
    """
    SQLAlchemy database model for storing student feedback NLP analysis records.
    Anonymous: No student names, emails, or personal identifiers stored.
    """
    __tablename__ = "analysis_records"

    id = Column(String(64), primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    sentiment_label = Column(String(32), nullable=False)
    sentiment_scores = Column(JSON, nullable=False)
    emotion_results = Column(JSON, nullable=False)
    
    # Core signal dimension scores
    stress_score = Column(Float, nullable=False, default=0.0)
    cognitive_overload_score = Column(Float, nullable=False, default=0.0)
    frustration_score = Column(Float, nullable=False, default=0.0)
    disengagement_score = Column(Float, nullable=False, default=0.0)
    workload_difficulty_score = Column(Float, nullable=False, default=0.0)
    choice_overload_score = Column(Float, nullable=False, default=0.0)
    time_pressure_score = Column(Float, nullable=False, default=0.0)
    
    # High-level ratings & primary concern
    overall_severity = Column(String(16), nullable=False, index=True)
    severity_reason = Column(Text, nullable=True)
    primary_concern = Column(String(64), nullable=False, index=True)
    primary_concern_score = Column(Float, nullable=False, default=0.0)
    
    # Interpretable output
    evidence = Column(JSON, nullable=False)
    explanation = Column(Text, nullable=False)
    student_insight = Column(Text, nullable=False)
    
    # Metadata timestamp
    created_at = Column(DateTime(timezone=True), default=datetime.now, index=True)
