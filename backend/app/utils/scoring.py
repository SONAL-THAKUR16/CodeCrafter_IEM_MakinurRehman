import re
from typing import Dict, Tuple
from app.schemas.analysis import AcademicSignals, PrimaryConcern

INTENSITY_BOOSTERS = {
    "extremely": 1.40,
    "severely": 1.40,
    "incredibly": 1.35,
    "completely": 1.30,
    "totally": 1.30,
    "very": 1.25,
    "heavy": 1.20,
    "too much": 1.25,
    "too many": 1.25,
    "really": 1.20,
    "so": 1.15
}

INTENSITY_DIMINISHERS = {
    "slightly": 0.55,
    "a little": 0.60,
    "somewhat": 0.65,
    "mildly": 0.65,
    "kind of": 0.70,
    "minor": 0.65,
    "one assignment": 0.70,
    "marginally": 0.65
}

SEVERITY_THRESHOLDS = {
    "HIGH": 0.67,
    "MODERATE": 0.34,
    "LOW": 0.00
}


def calculate_intensity_multiplier(text: str) -> float:
    """
    Scans text for intensity modifiers (boosters and diminishers) and returns a scaling factor.
    Baseline multiplier is 1.0.
    """
    text_lower = text.lower()
    multiplier = 1.0
    
    for word, boost in INTENSITY_BOOSTERS.items():
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            multiplier = max(multiplier, boost)
            
    for word, dim in INTENSITY_DIMINISHERS.items():
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            multiplier = min(multiplier, dim)
            
    if text.isupper() and len(text) > 10:
        multiplier = min(multiplier * 1.15, 1.45)
        
    return round(multiplier, 2)


def determine_overall_severity(signals: AcademicSignals) -> str:
    """
    Determines overall academic severity level (LOW, MODERATE, HIGH)
    from maximum signal score.
    """
    scores = [
        signals.stress,
        signals.cognitive_overload,
        signals.frustration,
        signals.disengagement,
        signals.workload_difficulty,
        signals.choice_overload,
        signals.time_pressure
    ]
    max_score = max(scores) if scores else 0.0

    if max_score >= SEVERITY_THRESHOLDS["HIGH"]:
        return "HIGH"
    elif max_score >= SEVERITY_THRESHOLDS["MODERATE"]:
        return "MODERATE"
    else:
        return "LOW"


def determine_primary_concern(signals: AcademicSignals) -> PrimaryConcern:
    """
    Identifies the single strongest academic experience concern.
    Returns PrimaryConcern(label=..., score=...).
    """
    mapping = {
        "time_pressure": signals.time_pressure,
        "cognitive_overload": signals.cognitive_overload,
        "workload_pressure": signals.workload_difficulty,
        "choice_difficulty": signals.choice_overload,
        "frustration": signals.frustration,
        "disengagement": signals.disengagement,
        "general_stress": signals.stress
    }
    
    sorted_concerns = sorted(mapping.items(), key=lambda item: item[1], reverse=True)
    top_label, top_score = sorted_concerns[0]
    
    if top_score < 0.30:
        return PrimaryConcern(label="none", score=0.0)
        
    return PrimaryConcern(label=top_label, score=round(top_score, 2))


def determine_severity_reason(
    overall_severity: str,
    signals: AcademicSignals,
    primary_concern: PrimaryConcern
) -> str:
    """
    Generates a clear data-driven explanation for the overall severity rating.
    """
    if overall_severity == "HIGH":
        if primary_concern.label != "none":
            formatted_label = primary_concern.label.replace('_', ' ')
            return f"Multiple workload and cognitive indicators were detected, with {formatted_label} as the primary distress signal."
        return "High levels of academic distress and task pressure were detected in the text."
    elif overall_severity == "MODERATE":
        if primary_concern.label != "none":
            formatted_label = primary_concern.label.replace('_', ' ')
            return f"Moderate academic friction detected, primarily driven by {formatted_label}."
        return "Moderate academic difficulty signals detected in student feedback."
    else:
        return "Student feedback reflects a manageable workload with minimal signs of academic distress."


def generate_student_insight(
    sentiment_label: str,
    signals: AcademicSignals,
    primary_concern: PrimaryConcern
) -> str:
    """
    Generates a neutral, non-clinical summary insight statement using tentative wording.
    """
    if sentiment_label == "mixed":
        return "The response indicates mixed academic sentiment, balancing positive engagement with specific workload or time management pressures."
    elif primary_concern.label != "none":
        formatted_label = primary_concern.label.replace('_', ' ')
        return f"The response suggests elevated {formatted_label} and potential difficulty balancing academic tasks."
    elif sentiment_label == "positive":
        return "The response contains mostly positive academic sentiment with limited signs of workload difficulty."
    else:
        return "The response shows manageable academic sentiment with low overall concern."
