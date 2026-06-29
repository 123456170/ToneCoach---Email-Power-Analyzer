# email_parser.py
import re
from typing import Dict, List

def parse_email(raw_text: str) -> Dict:
    """Parse raw email text into structured components."""
    lines = raw_text.strip().split('\n')
    
    subject = ""
    greeting = ""
    body_paragraphs = []
    action_requests = []
    sign_off = ""
    
    current_body = []
    in_body = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Subject detection
        if line.lower().startswith("subject:") or re.match(r'^re:|fw:', line, re.I):
            subject = line
            continue
        
        # Greeting
        if re.match(r'^(hi|hello|dear|hey)[\s,]', line, re.I) and len(greeting) < 5:
            greeting = line
            in_body = True
            continue
        
        # Sign off
        if re.match(r'^(best|regards|thanks|cheers|sincerely|warmly)', line, re.I):
            sign_off = line
            continue
        
        if in_body:
            current_body.append(line)
            
            # Action request detection
            if any(word in line.lower() for word in ["please", "could you", "would you", "i need", "can you", "let me know"]):
                action_requests.append(line)
    
    body_paragraphs = [" ".join(current_body)] if current_body else []
    
    word_count = len(re.findall(r'\w+', raw_text))
    sentence_count = len(re.split(r'[.!?]+', raw_text))
    
    return {
        "subject": subject,
        "greeting": greeting,
        "body_paragraphs": body_paragraphs,
        "body": " ".join(body_paragraphs),
        "action_requests": action_requests,
        "sign_off": sign_off,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "raw": raw_text
    }