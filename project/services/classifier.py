"""Rule-based symptom classifier module."""
from typing import Dict, Tuple


SYMPTOM_RULES: Dict[str, Dict[str, float]] = {
    "fungal infection": {"itching": 0.25, "rashes": 0.25, "redness": 0.2, "burning": 0.2},
    "bacterial dermatitis": {"swelling": 0.3, "redness": 0.3, "burning": 0.2},
    "viral rash": {"rashes": 0.25, "fever": 0.25, "itching": 0.15},
    "protozoan skin lesion": {"swelling": 0.3, "ulcer": 0.3, "redness": 0.2},
}


def classify_from_symptoms(symptoms_text: str) -> Tuple[str, float]:
    """Simple weighted keyword matching for non-image diagnosis."""
    tokens = symptoms_text.lower().replace(",", " ").split()

    best_disease = "fungal infection"
    best_score = 0.1

    for disease_name, keyword_map in SYMPTOM_RULES.items():
        score = sum(weight for keyword, weight in keyword_map.items() if keyword in tokens)
        if score > best_score:
            best_score = score
            best_disease = disease_name

    return best_disease, min(0.99, max(0.35, best_score + 0.35))
