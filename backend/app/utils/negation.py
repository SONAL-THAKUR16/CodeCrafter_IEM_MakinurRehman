import re
from typing import List, Tuple, Set

# Comprehensive English negation triggers
NEGATION_TERMS = {
    "not", "no", "never", "cannot", "can't", "don't", "doesn't", "didn't",
    "isn't", "aren't", "wasn't", "weren't", "won't", "wouldn't", "shouldn't",
    "couldn't", "without", "hardly", "scarcely", "barely", "lack", "lacks", "no problems", "no problem"
}

# Clause boundaries that terminate negation scope
CLAUSE_BOUNDARIES = {".", ",", ";", "!", "?", "but", "however", "although", "yet", "except"}


def is_phrase_negated(phrase: str, full_text: str) -> bool:
    """
    Checks whether a target concept or phrase in full_text is governed by a preceding negation.
    
    Examples:
      is_phrase_negated("stressed", "I am not stressed about the exam") -> True
      is_phrase_negated("workload", "I don't have any problems with the workload") -> True
      is_phrase_negated("stressed", "I am extremely stressed about the exam") -> False
    """
    text_lower = full_text.lower()
    phrase_lower = phrase.lower()

    # Direct negation patterns check
    negated_patterns = [
        rf"\b(not|no|never|don't|doesn't|didn't|isn't|aren't|wasn't|weren't|without)\s+(?:any\s+)?(?:feel\s+)?(?:causing\s+)?{re.escape(phrase_lower)}\b",
        rf"\b(don't|no|without)\s+(?:have\s+)?(?:any\s+)?(?:problems?|issue|difficulty)\s+(?:with\s+)?(?:the\s+)?{re.escape(phrase_lower)}\b"
    ]
    for pattern in negated_patterns:
        if re.search(pattern, text_lower):
            return True

    tokens = re.findall(r"\b\w+\b|[.,;!?]", text_lower)
    phrase_tokens = re.findall(r"\b\w+\b", phrase_lower)
    if not phrase_tokens:
        return False
    
    target_token = phrase_tokens[0]
    
    for idx, token in enumerate(tokens):
        if token == target_token:
            # Look backwards up to 5 tokens for a negation word
            window_start = max(0, idx - 5)
            window = tokens[window_start:idx]
            
            # Truncate window if clause boundary is present
            for w in window:
                if w in CLAUSE_BOUNDARIES:
                    window = window[window.index(w) + 1:]
            
            if any(w in NEGATION_TERMS for w in window):
                return True
                
    return False


def get_negated_concepts(text: str) -> Set[str]:
    """
    Returns set of core academic concept keywords that are negated in text.
    """
    concepts = [
        "stressed", "stress", "overwhelmed", "frustrated", "frustration",
        "overloaded", "overload", "difficult", "difficulty", "problem", "problems",
        "workload", "concentrate", "time"
    ]
    negated_set = set()
    for concept in concepts:
        if is_phrase_negated(concept, text):
            negated_set.add(concept)
    return negated_set
