from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class SentimentScores(BaseModel):
    """Normalized probability breakdown for sentiment levels."""
    positive: float = Field(0.0, ge=0.0, le=1.0)
    neutral: float = Field(0.0, ge=0.0, le=1.0)
    negative: float = Field(0.0, ge=0.0, le=1.0)


class SentimentAnalysis(BaseModel):
    """Sentiment classification result supporting mixed contexts."""
    label: str = Field(..., description="Dominant sentiment label: positive, neutral, negative, or mixed")
    scores: SentimentScores = Field(..., description="Confidence scores for sentiment classes")


class EmotionScore(BaseModel):
    """Individual emotion detection score."""
    label: str = Field(..., description="Emotion category (e.g. sadness, fear, joy, anger, neutral)")
    score: float = Field(..., ge=0.0, le=1.0, description="Model confidence score for emotion")


class AcademicSignals(BaseModel):
    """Normalized scores (0 to 1) across core academic experience dimensions."""
    stress: float = Field(..., ge=0.0, le=1.0, description="Level of stress indicated in text")
    cognitive_overload: float = Field(..., ge=0.0, le=1.0, description="Degree of cognitive overload or mental fatigue")
    frustration: float = Field(..., ge=0.0, le=1.0, description="Level of academic frustration")
    disengagement: float = Field(..., ge=0.0, le=1.0, description="Degree of academic disengagement or demotivation")
    workload_difficulty: float = Field(..., ge=0.0, le=1.0, description="Workload volume or coursework difficulty")
    choice_overload: float = Field(0.0, ge=0.0, le=1.0, description="Difficulty prioritizing or selecting tasks")
    time_pressure: float = Field(0.0, ge=0.0, le=1.0, description="Urgent deadline or time scarcity pressure")


class AcademicContextFlags(BaseModel):
    """Boolean indicator flags for key academic context dimensions."""
    workload_pressure: bool = Field(False, description="Presence of heavy workload or assignment pressure")
    time_pressure: bool = Field(False, description="Presence of upcoming deadlines or urgent time constraints")
    choice_difficulty: bool = Field(False, description="Difficulty prioritizing or deciding between tasks")
    cognitive_load: bool = Field(False, description="Mental fatigue or inability to concentrate")
    frustration: bool = Field(False, description="Frustration or irritation with academic structure")
    disengagement: bool = Field(False, description="Loss of interest or participation")


class PrimaryConcern(BaseModel):
    """Strongest detected academic experience concern."""
    label: str = Field("none", description="Primary concern category")
    score: float = Field(0.0, ge=0.0, le=1.0, description="Intensity score of primary concern")


class EvidenceItem(BaseModel):
    """Interpretable contextual evidence extracted directly from student feedback."""
    type: Optional[str] = Field(None, description="Legacy type field for backwards compatibility")
    category: str = Field(..., description="Target academic/emotional dimension")
    evidence: str = Field(..., description="Exact phrase or text snippet extracted from feedback")
    impact: str = Field(..., description="Severity impact of evidence: high, medium, or low")


class AnalyzeRequest(BaseModel):
    """Input payload for student academic feedback analysis."""
    text: str = Field(
        ...,
        description="Student academic feedback text (anonymous, no PII required)",
        min_length=1,
        max_length=5000,
        examples=["I enjoy this subject, but I have too many assignments and I don't know what to prioritize."]
    )

    @field_validator("text")
    @classmethod
    def validate_non_empty_text(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Feedback text cannot be empty or whitespace only.")
        return stripped


class AnalyzeResult(BaseModel):
    """Complete context-aware NLP analysis breakdown for student academic experience."""
    sentiment: SentimentAnalysis = Field(..., description="Sentiment classification")
    emotions: List[EmotionScore] = Field(default_factory=list, description="Top detected emotion classes")
    signals: AcademicSignals = Field(..., description="Calculated academic experience dimension scores")
    academic_context: AcademicContextFlags = Field(..., description="Boolean flags for academic context categories")
    primary_concern: PrimaryConcern = Field(..., description="Strongest detected academic concern")
    overall_severity: str = Field(..., description="Overall severity rating: LOW, MODERATE, or HIGH")
    severity_reason: str = Field(..., description="Data-driven reason for assigned overall severity")
    evidence: List[EvidenceItem] = Field(default_factory=list, description="Extracted phrases from actual student input")
    explanation: str = Field(..., description="Human-readable explanation of detected signals")
    student_insight: str = Field(..., description="Non-clinical, neutral summary insight for student feedback")
    disclaimer: str = Field(
        "This system identifies linguistic and academic experience signals. It is not a medical or psychological diagnosis system.",
        description="Notice clarifying system intent"
    )


class AnalyzeResponse(BaseModel):
    """API response wrapper for student feedback analysis."""
    success: bool = Field(True, description="Indicates successful analysis")
    analysis_id: str = Field(..., description="Unique identifier for analysis transaction")
    analysis: AnalyzeResult = Field(..., description="Structured NLP analysis result")


class HistoryItem(BaseModel):
    """Summary of a historical analysis session."""
    analysis_id: str
    created_at: str
    overall_severity: str
    primary_concern: str
    stress: float
    workload_difficulty: float
    text_snippet: Optional[str] = Field(None, description="Short truncated snippet of input text")


class HistoryResponse(BaseModel):
    """Response wrapper for analysis history."""
    success: bool = True
    count: int = 0
    items: List[HistoryItem] = Field(default_factory=list, description="History items list")
    history: List[HistoryItem] = Field(default_factory=list, description="Backwards compatible alias for items")


class DashboardSummaryData(BaseModel):
    """Calculated dashboard statistics from stored database records."""
    total_analyses: int
    average_stress: float
    average_cognitive_overload: float
    average_frustration: float
    average_disengagement: float
    average_workload_difficulty: float
    average_choice_overload: float
    average_time_pressure: float
    severity_distribution: Dict[str, int]
    most_common_concern: str


class DashboardSummaryResponse(BaseModel):
    """API response wrapper for dashboard summary statistics."""
    success: bool = True
    summary: DashboardSummaryData


class TrendPoint(BaseModel):
    """Data point for trend chart visualization."""
    analysis_id: str
    created_at: str
    stress: float
    cognitive_overload: float
    frustration: float
    workload_difficulty: float
    overall_severity: str


class DashboardTrendsResponse(BaseModel):
    """API response wrapper for dashboard trend data."""
    success: bool = True
    count: int = 0
    trends: List[TrendPoint] = Field(default_factory=list)
