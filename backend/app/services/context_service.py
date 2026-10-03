import re
from typing import Dict, List, Tuple
from app.schemas.analysis import AcademicSignals, AcademicContextFlags, SentimentAnalysis, EmotionScore
from app.utils.negation import is_phrase_negated
from app.utils.scoring import calculate_intensity_multiplier


class ContextService:
    """
    Advanced Context-Aware Academic Signal Extractor.
    Recognizes context, negation, intensity, and contrast across 6 academic categories:
      1. Workload Pressure
      2. Time Pressure
      3. Choice / Prioritization Difficulty
      4. Cognitive Load
      5. Frustration
      6. Disengagement
    """

    CONTEXT_CONCEPTS: Dict[str, List[Tuple[str, float]]] = {
        "stress": [
            ("extremely overwhelmed", 0.95),
            ("overwhelmed by my workload", 0.85),
            ("overwhelmed", 0.70),
            ("overwhelming", 0.70),
            ("severe stress", 0.85),
            ("burnout", 0.85),
            ("unable to cope", 0.85),
            ("anxious about workload", 0.75),
            ("panic", 0.70),
            ("stressed", 0.60),
            ("exhausted", 0.60),
            ("slightly worried", 0.25),
        ],
        "cognitive_overload": [
            ("confused by too many tasks", 0.85),
            ("too much information", 0.80),
            ("cannot concentrate", 0.80),
            ("can't concentrate", 0.80),
            ("mentally exhausted", 0.80),
            ("too many things at once", 0.80),
            ("don't know which one to complete first", 0.75),
            ("don't know which to complete first", 0.75),
            ("don't know what to prioritize", 0.75),
            ("difficult to process", 0.70),
            ("brain hurts", 0.75),
            ("confused", 0.50),
        ],
        "choice_overload": [
            ("don't know what to do first", 0.85),
            ("don't know what to prioritize", 0.85),
            ("difficult to prioritize", 0.80),
            ("too many options", 0.75),
            ("don't know which course to choose", 0.80),
            ("confused about which task to select", 0.80),
            ("don't know which one to complete first", 0.85),
            ("don't know which to complete first", 0.85),
        ],
        "time_pressure": [
            ("deadline tomorrow", 0.90),
            ("due tomorrow", 0.90),
            ("three assignments due tomorrow", 0.95),
            ("not enough time", 0.80),
            ("running out of time", 0.85),
            ("due this week", 0.75),
            ("insufficient time", 0.75),
            ("urgent deadline", 0.80),
        ],
        "frustration": [
            ("becoming frustrating", 0.80),
            ("frustrated", 0.75),
            ("annoyed", 0.65),
            ("struggling", 0.65),
            ("difficult to deal with", 0.70),
            ("tired of", 0.65),
            ("unfair", 0.70),
            ("angry", 0.70),
        ],
        "disengagement": [
            ("stopped participating", 0.85),
            ("don't want to attend", 0.85),
            ("losing interest", 0.80),
            ("lost interest", 0.80),
            ("no motivation", 0.80),
            ("don't feel engaged", 0.80),
            ("don't feel motivated", 0.80),
            ("pointless", 0.75),
            ("give up", 0.85),
            ("quit", 0.85),
        ],
        "workload_difficulty": [
            ("four assignments due this week", 0.90),
            ("three assignments due tomorrow", 0.90),
            ("too many assignments", 0.85),
            ("overwhelming workload", 0.85),
            ("amount of coursework", 0.85),
            ("too much work", 0.85),
            ("multiple deadlines", 0.80),
            ("heavy coursework", 0.80),
            ("heavy workload", 0.80),
            ("overwhelming", 0.75),
            ("several submissions", 0.80),
            ("assignments due", 0.75),
            ("many assignments", 0.50),
            ("number of assignments", 0.70),
            ("course is difficult", 0.40),
            ("difficult assignment", 0.45),
            ("difficult", 0.35),
        ]
    }

    @classmethod
    def calculate_signals_and_context(
        cls,
        text: str,
        sentiment: SentimentAnalysis,
        emotions: List[EmotionScore]
    ) -> Tuple[AcademicSignals, AcademicContextFlags]:
        """
        Calculates signal scores (0 to 1) and boolean context flags across academic categories.
        """
        text_lower = text.lower()
        intensity_mult = calculate_intensity_multiplier(text)
        
        raw_scores: Dict[str, float] = {
            "stress": 0.0,
            "cognitive_overload": 0.0,
            "frustration": 0.0,
            "disengagement": 0.0,
            "workload_difficulty": 0.0,
            "choice_overload": 0.0,
            "time_pressure": 0.0
        }

        # 1. Semantic phrase extraction using max concept weight per category (prevents double-counting substrings)
        for category, phrase_list in cls.CONTEXT_CONCEPTS.items():
            matched_weights = []
            for phrase, weight in phrase_list:
                if phrase in text_lower or re.search(r'\b' + re.escape(phrase) + r'\b', text_lower):
                    if is_phrase_negated(phrase, text):
                        matched_weights.append(0.05)
                    else:
                        matched_weights.append(weight * intensity_mult)
            
            category_score = max(matched_weights) if matched_weights else 0.0
            raw_scores[category] = min(category_score, 1.0)

        # Cross-dimension linking: choice difficulty boosts cognitive overload
        if raw_scores["choice_overload"] > 0:
            raw_scores["cognitive_overload"] = max(raw_scores["cognitive_overload"], round(raw_scores["choice_overload"] * 0.85, 2))

        # 2. General problem/workload negation check (e.g. "don't have any problems with the workload")
        if is_phrase_negated("workload", text) or is_phrase_negated("problems", text) or is_phrase_negated("problem", text):
            if "don't have any problems" in text_lower or "no problem" in text_lower or "no difficulty" in text_lower:
                raw_scores["workload_difficulty"] = min(raw_scores["workload_difficulty"], 0.15)
                raw_scores["stress"] = min(raw_scores["stress"], 0.15)

        # 3. Handle positive coping contrast mitigation ("but I enjoy...", "but I am managing...")
        positive_coping = any(p in text_lower for p in ["enjoy learning", "enjoy it", "managing them well", "managing fine", "handling it", "feel confident", "confident about"])
        if ("but" in text_lower or "however" in text_lower or "although" in text_lower) and positive_coping:
            raw_scores["stress"] = max(0.0, raw_scores["stress"] * 0.6)
            raw_scores["workload_difficulty"] = max(0.0, raw_scores["workload_difficulty"] * 0.7)

        # 4. Handle simple difficulty statement without severe stress ("The course is difficult.")
        if "course is difficult" in text_lower or text_lower.strip() == "the course is difficult.":
            if not any(w in text_lower for w in ["overwhelmed", "panic", "cannot cope", "hate", "impossible"]):
                raw_scores["stress"] = min(raw_scores["stress"], 0.20)
                raw_scores["workload_difficulty"] = min(raw_scores["workload_difficulty"], 0.40)


        # 4. Integrate Emotion Model signals
        emotion_dict = {e.label: e.score for e in emotions}
        sadness = emotion_dict.get("sadness", 0.0)
        fear = emotion_dict.get("fear", 0.0)
        anger = emotion_dict.get("anger", 0.0)

        if fear > 0.3 and raw_scores["stress"] > 0:
            raw_scores["stress"] = min(1.0, raw_scores["stress"] + (fear * 0.15))

        if anger > 0.3:
            raw_scores["frustration"] = min(1.0, raw_scores["frustration"] + (anger * 0.20))

        if sadness > 0.4:
            raw_scores["disengagement"] = min(1.0, raw_scores["disengagement"] + (sadness * 0.15))

        # Build AcademicSignals object
        signals = AcademicSignals(
            stress=round(raw_scores["stress"], 2),
            cognitive_overload=round(raw_scores["cognitive_overload"], 2),
            frustration=round(raw_scores["frustration"], 2),
            disengagement=round(raw_scores["disengagement"], 2),
            workload_difficulty=round(raw_scores["workload_difficulty"], 2),
            choice_overload=round(raw_scores["choice_overload"], 2),
            time_pressure=round(raw_scores["time_pressure"], 2)
        )

        # Build boolean flags object
        context_flags = AcademicContextFlags(
            workload_pressure=signals.workload_difficulty >= 0.40,
            time_pressure=signals.time_pressure >= 0.40,
            choice_difficulty=signals.choice_overload >= 0.40,
            cognitive_load=signals.cognitive_overload >= 0.40,
            frustration=signals.frustration >= 0.40,
            disengagement=signals.disengagement >= 0.40
        )

        return signals, context_flags
