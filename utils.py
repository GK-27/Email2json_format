# import necessary modules
from collections import OrderedDict
import re
# define function
def mask_pii(text):
    entities = []
    masked_text = text

    # Define regex patterns for detecting different types of PII

    patterns = {
        "EMAIL": r'[\w\.-]+@[\w\.-]+',
        "PHONE": r'\b\d{10}\b',
        "NAME": r'\b([A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,}){0,2})\b',
        "DOB": r'\b(?:\d{2}[/-]){2}\d{4}\b',
        "AADHAR_NUM": r'\b\d{4}\s\d{4}\s\d{4}\b',
        "CREDIT_DEBIT_NO": r'\b(?:\d[ -]*?){13,16}\b',
        "CVV_NO": r'\b\d{3}\b',
        "EXPIRY_NO": r'\b(0[1-9]|1[0-2])/\d{2}\b'
    }

    matches = []

 # Iterate through each pattern and find matching PII in the text
    for label, pattern in patterns.items():
        for match in re.finditer(pattern, masked_text):
            matches.append({
                "start": match.start(),
                "end": match.end(),
                "label": label,
                "text": match.group()
            })

 # Sort matches by their start position (reverse order for correct replacement)
    matches.sort(key=lambda m: m["start"], reverse=True)
# Replace each match with a placeholder in the masked text
    for idx, match in enumerate(matches):
        placeholder = f"[{match['label']}{idx}]"
        masked_text = masked_text[:match["start"]] + placeholder + masked_text[match["end"]:]
        
        # Create an OrderedDict for each entity to maintain order of key
        entity = OrderedDict([
            ("position", [match["start"], match["start"] + len(placeholder)]),
            ("classification", match["label"]),
            ("entity", match["text"])
        ])
        entities.append(entity)
# return the masked_text and entites
    return masked_text, list(reversed(entities))