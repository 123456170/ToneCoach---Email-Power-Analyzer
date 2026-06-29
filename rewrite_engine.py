# rewrite_engine.py
from typing import List, Dict
import re

REWRITE_RULES = {
    "sorry to bother you": {
        "direct": "",
        "diplomatic": "I wanted to follow up on",
        "warm": "I hope you are doing well -"
    },
    "per my last email": {
        "direct": "As mentioned previously,",
        "diplomatic": "To recap from my previous email,",
        "warm": "I wanted to revisit something I mentioned -"
    },
    "i was wondering if maybe": {
        "direct": "Please",
        "diplomatic": "Could you",
        "warm": "Would you be able to"
    },
    "whenever you get a chance": {
        "direct": "by EOD Friday",
        "diplomatic": "when you have a moment this week",
        "warm": "at your earliest convenience"
    },
    "just wanted to check": {
        "direct": "Following up:",
        "diplomatic": "I am following up on",
        "warm": "I wanted to touch base about"
    },
    # Add 30+ more rules here as needed
}

def rewrite_sentence(sentence: str, issues: List, target_register: str = "Diplomatic") -> Dict:
    """Rewrite a single sentence based on detected issues."""
    rewritten = sentence
    changes = []
    reg_key = target_register.lower()
    
    for original, variants in REWRITE_RULES.items():
        if original.lower() in sentence.lower():
            replacement = variants.get(reg_key, variants.get("diplomatic", original))
            rewritten = re.sub(re.escape(original), replacement, rewritten, flags=re.I)
            changes.append(f"Replaced '{original}'")
    
    return {
        "original": sentence,
        "rewritten": rewritten,
        "changes_made": changes
    }

def rewrite_full_email(email_text: str, issues: List, target_register: str) -> str:
    """Apply rewrites across the entire email."""
    rewritten = email_text
    for orig, variants in REWRITE_RULES.items():
        repl = variants.get(target_register.lower(), variants.get("diplomatic", orig))
        rewritten = re.sub(re.escape(orig), repl, rewritten, flags=re.I)
    return rewritten

def get_rewrite_suggestions(email_text: str, issues: List) -> List[Dict]:
    """Generate suggestions for each sentence."""
    sentences = re.split(r'(?<=[.!?])\s+', email_text)
    return [rewrite_sentence(s, issues, "Diplomatic") for s in sentences if s.strip()]