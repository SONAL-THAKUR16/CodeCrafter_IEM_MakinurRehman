import re
from typing import List, Tuple
from app.schemas.analysis import AcademicSignals, EvidenceItem
from app.utils.negation import is_phrase_negated


class ExplainabilityService:
    """
    Context-aware phrase extraction engine.
    Extracts authentic evidence snippets directly from student feedback text
    without fabricating phrases.
    """

    EVIDENCE_PATTERNS: List[Tuple[str, str]] = [
        # (phrase/pattern, category)
        ("three assignments due tomorrow", "time_pressure"),
        ("due tomorrow", "time_pressure"),
        ("deadline tomorrow", "time_pressure"),
        ("due this week", "time_pressure"),
        ("not enough time", "time_pressure"),
        ("running out of time", "time_pressure"),
        
        ("don't know what to prioritize", "choice_difficulty"),
        ("don't know what to do first", "choice_difficulty"),
        ("don't know which one to complete first", "choice_difficulty"),
        ("don't know which to complete first", "choice_difficulty"),
        ("difficult to prioritize", "choice_difficulty"),
        ("confused about which task to select", "choice_difficulty"),
        
        ("amount of coursework", "workload_pressure"),
        ("amount of work", "workload_pressure"),
        ("too many assignments", "workload_pressure"),
        ("three assignments due", "workload_pressure"),
        ("four assignments due", "workload_pressure"),
        ("number of assignments", "workload_pressure"),
        ("heavy workload", "workload_pressure"),
        ("heavy coursework", "workload_pressure"),
        ("too much work", "workload_pressure"),
        ("assignments due", "workload_pressure"),
        ("course is difficult", "course_difficulty"),
        
        ("cannot concentrate", "cognitive_overload"),
        ("can't concentrate", "cognitive_overload"),
        ("too many things at once", "cognitive_overload"),
        ("too much information", "cognitive_overload"),
        ("confused by too many tasks", "cognitive_overload"),
        ("mentally exhausted", "cognitive_overload"),
        
        ("extremely overwhelmed", "stress"),
        ("overwhelmed", "stress"),
        ("anxious about workload", "stress"),
        ("unable to cope", "stress"),
        ("burnout", "stress"),
        ("slightly worried", "stress_mild"),
        ("not stressed", "stress_negated"),
        
        ("becoming frustrating", "frustration"),
        ("frustrated", "frustration"),
        ("annoying", "frustration"),
        ("struggling", "frustration"),
        ("unfair", "frustration"),
        
        ("losing interest", "disengagement"),
        ("lost interest", "disengagement"),
        ("stopped participating", "disengagement"),
        ("don't want to attend", "disengagement"),
        ("don't feel motivated", "disengagement"),
        ("no motivation", "disengagement"),

        ("enjoying it and learning a lot", "positive_engagement"),
        ("enjoy this subject", "positive_engagement"),
        ("really enjoy the course", "positive_engagement"),
        ("enjoying this course", "positive_engagement"),
        ("managing them well", "positive_coping"),
        ("confident about my assignments", "positive_engagement"),
        ("learning a lot", "positive_engagement"),
        ("don't have any problems", "positive_coping"),
    ]

    @classmethod
    def generate_explainability(
        cls,
        text: str,
        signals: AcademicSignals,
        overall_severity: str
    ) -> Tuple[List[EvidenceItem], str]:
        """
        Extracts evidence phrases present in text and formats clear explanations.
        """
        text_lower = text.lower()
        evidence_list: List[EvidenceItem] = []
        seen_phrases = set()

        for pattern, category in cls.EVIDENCE_PATTERNS:
            if pattern in text_lower and pattern not in seen_phrases:
                seen_phrases.add(pattern)
                
                is_negated = is_phrase_negated(pattern, text)
                
                if category == "stress_negated" or is_negated:
                    evidence_list.append(
                        EvidenceItem(
                            type="stress",
                            category="stress",
                            evidence=f"'{pattern}' (negation recognized)",
                            impact="low"
                        )
                    )
                elif category == "stress_mild":
                    evidence_list.append(
                        EvidenceItem(
                            type="stress",
                            category="stress",
                            evidence=pattern,
                            impact="low"
                        )
                    )
                elif category in ["positive_engagement", "positive_coping"]:
                    evidence_list.append(
                        EvidenceItem(
                            type="positive_sentiment",
                            category="positive_engagement",
                            evidence=pattern,
                            impact="low"
                        )
                    )
                else:
                    impact = "high" if overall_severity == "HIGH" else "medium"
                    evidence_list.append(
                        EvidenceItem(
                            type=category,
                            category=category,
                            evidence=pattern,
                            impact=impact
                        )
                    )

        # Fallback keyword extraction if no multi-word phrase matched
        if not evidence_list:
            for word in ["stressed", "overwhelmed", "assignments", "exam", "confused", "frustrating", "difficult", "enjoying", "managing"]:
                if re.search(r'\b' + word + r'\b', text_lower):
                    is_neg = is_phrase_negated(word, text)
                    impact = "low" if (is_neg or word in ["enjoying", "managing"]) else ("high" if overall_severity == "HIGH" else "medium")
                    evidence_list.append(
                        EvidenceItem(
                            type="keyword_signal",
                            category="keyword_signal",
                            evidence=f"'{word}' (negated)" if is_neg else word,
                            impact=impact
                        )
                    )

        # Build natural language explanation summary
        high_signals = []
        if signals.workload_difficulty >= 0.50:
            high_signals.append("Workload Pressure")
        if signals.time_pressure >= 0.50:
            high_signals.append("Time Pressure")
        if signals.cognitive_overload >= 0.50:
            high_signals.append("Cognitive Overload")
        if signals.choice_overload >= 0.50:
            high_signals.append("Prioritization Difficulty")
        if signals.stress >= 0.50:
            high_signals.append("Stress")
        if signals.frustration >= 0.50:
            high_signals.append("Frustration")
        if signals.disengagement >= 0.50:
            high_signals.append("Disengagement")

        if high_signals:
            explanation = (
                f"Linguistic analysis identified elevated indicators of {', '.join(high_signals)}. "
                f"Extracted evidence: {', '.join([f'\"{e.evidence}\"' for e in evidence_list[:3]])}. "
                f"Overall academic severity rating is {overall_severity}."
            )
        else:
            explanation = (
                f"Student feedback reflects a manageable workload with low academic distress. "
                f"Overall academic severity rating is {overall_severity}."
            )

        return evidence_list, explanation
