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
    # Normalize column names to lowercase for case-insensitive comparison
    normalized_cols = {str(c).strip().lower() for c in cols}
    missing = [c for c in REQUIRED_COLS if c not in normalized_cols]
    return missing
