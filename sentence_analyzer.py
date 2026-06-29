# sentence_analyzer.py
import re
from typing import List, Dict

def analyze_sentences(body_text: str) -> List[Dict]:
    """Break down body into sentences with tone flags."""
    sentences = re.split(r'(?<=[.!?])\s+', body_text)
    analyzed = []
    
    for sent in sentences:
        if not sent.strip():
            continue
        flags = []
        lower = sent.lower()
        if any(m in lower for m in ["sorry", "apologise"]):
            flags.append("OVER_APOLOGY")
        if any(m in lower for m in ["perhaps", "maybe", "wondering"]):
            flags.append("HEDGING")
        analyzed.append({
            "text": sent.strip(),
            "flags": flags,
            "length": len(sent.split())
        })
    return analyzed