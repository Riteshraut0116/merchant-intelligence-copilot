import re

REQUIRED_COLS = {"date","product_name","quantity_sold","price","revenue"}

def validate_prompt_injection(text:str)->bool:
    patterns = [
        r"ignore previous instructions",
        r"disregard all",
        r"system prompt",
        r"<script>",
        r"DROP TABLE",
        r"';\s*DELETE\s+FROM"
    ]
    return not any(re.search(p, text, re.IGNORECASE) for p in patterns)

def validate_csv_columns(cols):
    missing = [c for c in REQUIRED_COLS if c not in cols]
    return missing
