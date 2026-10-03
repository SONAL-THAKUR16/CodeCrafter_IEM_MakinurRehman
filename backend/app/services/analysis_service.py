import logging
from app.schemas.analysis import AnalyzeResult
from app.services.sentence_service import SentenceService
from app.services.emotion_service import EmotionService
from app.services.context_service import ContextService
from app.services.explainability_service import ExplainabilityService
from app.utils.scoring import (
    determine_overall_severity,
    determine_primary_concern,
    determine_severity_reason,
    generate_student_insight
)

logger = logging.getLogger("student_analyzer_api")


class AnalysisService:
    """
    Master Context-Aware NLP Analysis Pipeline.
    
    Architecture:
      INPUT TEXT
      ↓ Validation
      ↓ Sentence-Level Sentiment & Contrast Analysis (SentenceService)
      ↓ Emotion Classification (EmotionService)
      ↓ Context-Aware Academic Signal & Flag Extraction (ContextService)
      ↓ Negation & Scope Parsing (negation.py)
      ↓ Intensity Scaling (scoring.py)
      ↓ Primary Concern Identification (scoring.py)
      ↓ Severity & Severity Reason Calculation (scoring.py)
      ↓ Explainability & Snippet Evidence Extraction (ExplainabilityService)
      ↓ Non-Clinical Student Insight Generation (scoring.py)
      ↓ API Response
    """

    @classmethod
    def analyze_text(cls, text: str) -> AnalyzeResult:
        """
        Executes end-to-end context-aware analysis pipeline on student feedback text.
        """
        logger.info("Executing Context-Aware NLP pipeline...")

        # Step 1: Sentence & Clause Level Sentiment Analysis
        sentiment = SentenceService.analyze_sentence_sentiment(text)

        # Step 2: Emotion Classification
        emotions = EmotionService.analyze(text)

        # Step 3: Context Signals & Category Flags Extraction
        signals, academic_context = ContextService.calculate_signals_and_context(
            text=text,
            sentiment=sentiment,
            emotions=emotions
        )

        # Step 4: Primary Concern Identification
        primary_concern = determine_primary_concern(signals)

        # Step 5: Overall Severity Rating & Severity Reason
        overall_severity = determine_overall_severity(signals)
        severity_reason = determine_severity_reason(
            overall_severity=overall_severity,
            signals=signals,
            primary_concern=primary_concern
        )

        # Step 6: Evidence Phrase Extraction & Explanation Summary
        evidence, explanation = ExplainabilityService.generate_explainability(
            text=text,
            signals=signals,
            overall_severity=overall_severity
        )

        # Step 7: Non-Clinical Student Summary Insight
        student_insight = generate_student_insight(
            sentiment_label=sentiment.label,
            signals=signals,
            primary_concern=primary_concern
        )

        return AnalyzeResult(
            sentiment=sentiment,
            emotions=emotions,
            signals=signals,
            academic_context=academic_context,
            primary_concern=primary_concern,
            overall_severity=overall_severity,
            severity_reason=severity_reason,
            evidence=evidence,
            explanation=explanation,
            student_insight=student_insight,
            disclaimer="This system identifies linguistic and academic experience signals. It is not a medical or psychological diagnosis system."
        )
