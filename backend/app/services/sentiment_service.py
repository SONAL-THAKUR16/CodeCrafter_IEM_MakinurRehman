import logging
from typing import Optional, Dict
from app.schemas.analysis import SentimentAnalysis, SentimentScores

logger = logging.getLogger("student_analyzer_api")

# Cached model pipeline singleton
_sentiment_pipeline = None
_model_failed = False


def _load_sentiment_model():
    """Loads the pretrained Hugging Face sentiment analysis model into memory once."""
    global _sentiment_pipeline, _model_failed
    if _sentiment_pipeline is not None or _model_failed:
        return _sentiment_pipeline

    try:
        from transformers import pipeline
        logger.info("Loading Hugging Face sentiment model (distilbert-base-uncased-finetuned-sst-2-english)...")
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
            return_all_scores=True
        )
        logger.info("Sentiment analysis model loaded successfully.")
    except Exception as exc:
        logger.warning(f"Unable to load Hugging Face sentiment model: {exc}. Falling back to lexicon sentiment analyzer.")
        _model_failed = True
        _sentiment_pipeline = None

    return _sentiment_pipeline


class SentimentService:
    """Service for sentiment classification using Hugging Face Transformers with resilient fallback."""

    POSITIVE_WORDS = {
        "enjoy", "enjoying", "confident", "good", "great", "excellent", "satisfied",
        "love", "happy", "accomplished", "clear", "helpful", "well", "fine", "positive"
    }
    
    NEGATIVE_WORDS = {
        "overwhelmed", "stressed", "frustrated", "confused", "impossible", "hate",
        "terrible", "horrible", "struggling", "bad", "difficult", "annoyed", "useless"
    }

    @classmethod
    def analyze(cls, text: str) -> SentimentAnalysis:
        pipeline_instance = _load_sentiment_model()
        if pipeline_instance is not None:
            try:
                truncated_text = text[:1000]
                raw_results = pipeline_instance(truncated_text)
                if isinstance(raw_results, list) and len(raw_results) > 0:
                    if isinstance(raw_results[0], list):
                        raw_results = raw_results[0]
                
                # Convert raw scores to dict
                score_dict: Dict[str, float] = {}
                for item in raw_results:
                    if isinstance(item, dict) and "label" in item and "score" in item:
                        label = item["label"].lower()
                        score_dict[label] = float(item["score"])
                
                pos_score = round(score_dict.get("positive", 0.0), 3)
                neg_score = round(score_dict.get("negative", 0.0), 3)
                neu_score = round(max(0.0, 1.0 - (pos_score + neg_score)), 3)
                
                # Determine dominant label
                if neg_score >= 0.50:
                    dominant = "negative"
                elif pos_score >= 0.50:
                    dominant = "positive"
                else:
                    dominant = "neutral"

                return SentimentAnalysis(
                    label=dominant,
                    scores=SentimentScores(
                        positive=pos_score,
                        neutral=neu_score,
                        negative=neg_score
                    )
                )
            except Exception as exc:
                logger.error(f"Error executing sentiment pipeline: {exc}. Using lexicon fallback.")

        # Resilient Lexicon Fallback
        return cls._fallback_sentiment(text)

    @classmethod
    def _fallback_sentiment(cls, text: str) -> SentimentAnalysis:
        """Rule/Lexicon based fallback for sentiment analysis."""
        text_lower = text.lower()
        words = text_lower.split()
        pos_count = sum(1 for w in cls.POSITIVE_WORDS if w in text_lower)
        neg_count = sum(1 for w in cls.NEGATIVE_WORDS if w in text_lower)
        
        # Check specific phrase indicators
        if "cannot concentrate" in text_lower or "can't concentrate" in text_lower or "too much work" in text_lower:
            neg_count += 2

        if pos_count > neg_count:
            pos_val = 0.82
            neg_val = 0.08
            neu_val = 0.10
            dominant = "positive"
        elif neg_count > pos_count:
            neg_val = 0.85
            pos_val = 0.05
            neu_val = 0.10
            dominant = "negative"
        else:
            pos_val = 0.20
            neg_val = 0.20
            neu_val = 0.60
            dominant = "neutral"

        return SentimentAnalysis(
            label=dominant,
            scores=SentimentScores(
                positive=pos_val,
                neutral=neu_val,
                negative=neg_val
            )
        )
