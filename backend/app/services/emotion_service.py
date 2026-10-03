import logging
from typing import List, Dict
from app.schemas.analysis import EmotionScore

logger = logging.getLogger("student_analyzer_api")

_emotion_pipeline = None
_emotion_failed = False


def _load_emotion_model():
    """Loads the pretrained Hugging Face emotion detection model once."""
    global _emotion_pipeline, _emotion_failed
    if _emotion_pipeline is not None or _emotion_failed:
        return _emotion_pipeline

    try:
        from transformers import pipeline
        logger.info("Loading Hugging Face emotion model (bhadresh-ps/distilbert-base-uncased-emotion)...")
        _emotion_pipeline = pipeline(
            "text-classification",
            model="bhadresh-ps/distilbert-base-uncased-emotion",
            return_all_scores=True
        )
        logger.info("Emotion analysis model loaded successfully.")
    except Exception as exc:
        logger.warning(f"Unable to load Hugging Face emotion model: {exc}. Using fallback emotion classifier.")
        _emotion_failed = True
        _emotion_pipeline = None

    return _emotion_pipeline


class EmotionService:
    """Service for emotion detection using Hugging Face Transformers with resilient fallback."""

    EMOTION_LEXICON = {
        "joy": ["enjoying", "confident", "happy", "excited", "love", "glad", "pleased", "great", "fine"],
        "sadness": ["depressed", "unhappy", "cry", "crying", "miserable", "lonely", "disappointed", "hopeless", "sad"],
        "anger": ["annoyed", "frustrated", "angry", "furious", "hate", "unfair", "irritated", "outraged"],
        "fear": ["anxious", "scared", "fear", "worried", "nervous", "terrified", "panic", "overwhelmed", "dread"],
        "surprise": ["shocked", "surprised", "unexpected", "amazed", "astonished"],
        "disgust": ["gross", "disgusted", "revolting", "nasty", "abhorrent"]
    }

    @classmethod
    def analyze(cls, text: str) -> List[EmotionScore]:
        """Analyzes input text and returns sorted list of detected emotion scores."""
        pipeline_instance = _load_emotion_model()
        
        if pipeline_instance is not None:
            try:
                truncated_text = text[:1000]
                raw_results = pipeline_instance(truncated_text)[0]
                
                emotions: List[EmotionScore] = []
                for item in raw_results:
                    label = item["label"].lower()
                    score = round(float(item["score"]), 3)
                    if score >= 0.05:  # Include relevant emotion signals
                        emotions.append(EmotionScore(label=label, score=score))
                        
                # Sort by score descending
                emotions.sort(key=lambda e: e.score, reverse=True)
                return emotions
            except Exception as exc:
                logger.error(f"Error executing emotion pipeline: {exc}. Using lexicon fallback.")

        # Fallback implementation
        return cls._fallback_emotions(text)

    @classmethod
    def _fallback_emotions(cls, text: str) -> List[EmotionScore]:
        """Lexicon-based fallback for emotion analysis."""
        words = text.lower().split()
        scores: Dict[str, float] = {}
        
        for emotion, keywords in cls.EMOTION_LEXICON.items():
            matches = sum(1 for w in words if any(kw in w for kw in keywords))
            if matches > 0:
                scores[emotion] = round(min(0.35 + (matches * 0.25), 0.90), 3)
                
        if not scores:
            scores["neutral"] = 0.85
            
        result = [EmotionScore(label=lbl, score=sc) for lbl, sc in scores.items()]
        result.sort(key=lambda e: e.score, reverse=True)
        return result
