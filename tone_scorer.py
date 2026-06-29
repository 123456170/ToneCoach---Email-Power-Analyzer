# tone_scorer.py
from typing import Dict, List, Any
import re

TONE_DIMENSIONS = {
    "assertiveness": {"weight": 0.25},
    "hedging": {"weight": 0.20},
    "passive_aggression": {"weight": 0.15},
    "over_apology": {"weight": 0.10},
    "solution_ownership": {"weight": 0.15},
    "clarity": {"weight": 0.15}
}

PASSIVE_AGGRESSION_MARKERS = [
    "per my last email", "as i mentioned", "as previously stated", "just a reminder",
    "noted", "sure", "fine", "as you know", "i would have thought", "obviously", "clearly"
]

OVER_APOLOGY_MARKERS = [
    "sorry to bother", "sorry for bothering", "i apologise for taking", "forgive me",
    "i hope i am not", "i hate to ask", "apologies for"
]

HEDGING_MARKERS = [
    "i was wondering if", "perhaps", "i suppose", "at your convenience",
    "whenever you have a moment", "not sure if right but", "just a thought",
    "could be", "if possible", "no rush"
]

def analyze_tone(email_data: Dict) -> Dict:
    body = email_data["body"].lower()
    
    # Passive aggression
    pa_count = sum(1 for marker in PASSIVE_AGGRESSION_MARKERS if marker in body)
    pa_score = max(0, 100 - pa_count * 8)
    
    # Over apology
    oa_count = sum(1 for marker in OVER_APOLOGY_MARKERS if marker in body)
    oa_score = max(0, 100 - oa_count * 15)
    
    # Hedging
    hedge_count = sum(1 for marker in HEDGING_MARKERS if marker in body)
    hedge_score = max(0, 100 - hedge_count * 7)
    
    # Assertiveness & Ownership (simplified)
    assert_score = 75  # Placeholder - would use more NLP
    ownership_score = 80
    
    dimensions = {
        "assertiveness": {"score": assert_score, "label": "Good"},
        "hedging": {"score": hedge_score, "label": "Moderate" if hedge_score < 70 else "Strong"},
        "passive_aggression": {"score": pa_score, "label": "Flagged" if pa_count > 1 else "Clean"},
        "over_apology": {"score": oa_score, "label": "Flagged" if oa_count > 1 else "Clean"},
        "solution_ownership": {"score": ownership_score, "label": "Strong"},
        "clarity": {"score": 85, "label": "Strong"}
    }
    
    overall_score = int(sum(d["score"] * TONE_DIMENSIONS[k]["weight"] for k, d in dimensions.items()))
    
    top_issues = [
        {"type": "Hedging", "description": f"Detected {hedge_count} softening phrases", "severity": "Medium"}
    ] if hedge_count > 2 else []
    
    return {
        "overall_score": overall_score,
        "dimensions": dimensions,
        "top_issues": top_issues,
        "issues": [{"type": "hedging", "count": hedge_count}]
    }