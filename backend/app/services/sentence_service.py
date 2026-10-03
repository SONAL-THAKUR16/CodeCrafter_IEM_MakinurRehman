import re
from typing import List, Tuple
from app.schemas.analysis import SentimentAnalysis, SentimentScores
from app.services.sentiment_service import SentimentService

CONTRAST_CONJUNCTIONS = {"but", "however", "although", "yet", "even though", "nevertheless", "on the other hand"}


class SentenceService:
    """
    Performs sentence-level & clause-level NLP analysis to recognize contrast,
    mixed emotional contexts, and multi-sentence structures.
    """

    POSITIVE_MARKERS = {"enjoy", "enjoying", "love", "confident", "learning a lot", "fine", "good", "great", "managing"}
    NEGATIVE_MARKERS = {"difficult", "too many assignments", "overwhelming", "overwhelmed", "frustrating", "stressed", "cannot concentrate", "can't concentrate", "hate", "struggling"}

    @classmethod
    def split_into_sentences(cls, text: str) -> List[str]:
        """Splits input text into individual sentences."""
        raw_sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in raw_sentences if s.strip()]

    @classmethod
    def analyze_sentence_sentiment(cls, text: str) -> SentimentAnalysis:
        """
        Analyzes full text and sentence/clause structure to identify mixed sentiment or contrast.
        """
        sentences = cls.split_into_sentences(text)
        text_lower = text.lower()
        
        has_contrast = any(re.search(r'\b' + re.escape(conj) + r'\b', text_lower) for conj in CONTRAST_CONJUNCTIONS)
        base_sentiment = SentimentService.analyze(text)

        # Check clause-level sentiments
        clause_sentiments: List[Tuple[str, SentimentAnalysis]] = []
        for sentence in sentences:
            if any(re.search(r'\b' + re.escape(conj) + r'\b', sentence.lower()) for conj in CONTRAST_CONJUNCTIONS):
                clauses = re.split(r'\b(?:but|however|although|yet)\b', sentence, flags=re.IGNORECASE)
                for clause in clauses:
                    if clause.strip():
                        clause_sentiments.append((clause.strip(), SentimentService.analyze(clause.strip())))
            else:
                clause_sentiments.append((sentence, SentimentService.analyze(sentence)))

        pos_clause_count = sum(1 for c in clause_sentiments if c[1].label == "positive" or any(re.search(r'\b' + re.escape(p) + r'\b', c[0].lower()) for p in cls.POSITIVE_MARKERS))
        neg_clause_count = sum(1 for c in clause_sentiments if c[1].label == "negative" or any(re.search(r'\b' + re.escape(n) + r'\b', c[0].lower()) for n in cls.NEGATIVE_MARKERS))

        # Mixed sentiment requires BOTH genuine positive and genuine negative elements
        if has_contrast or len(sentences) > 1:
            if pos_clause_count > 0 and neg_clause_count > 0:
                return SentimentAnalysis(
                    label="mixed",
                    scores=SentimentScores(
                        positive=0.45,
                        neutral=0.15,
                        negative=0.40
                    )
                )

        return base_sentiment
