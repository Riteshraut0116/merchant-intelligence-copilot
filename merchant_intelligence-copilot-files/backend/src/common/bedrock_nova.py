import json, boto3
from .config import AWS_REGION, TEMPERATURE, TOP_P, MAX_TOKENS

br = boto3.client("bedrock-runtime", region_name=AWS_REGION)

def nova_converse(model_id: str, system: str, user: str):
    # Uses Bedrock "converse" style payload (works for many models including Nova)
    # If your account requires a different schema, adjust here centrally.
    body = {
        "inferenceConfig": {
            "temperature": TEMPERATURE,
            "topP": TOP_P,
            "maxTokens": MAX_TOKENS
        },
        "messages": [
            {"role":"user","content":[{"text": user}]}
        ],
        "system": [{"text": system}]
    }
    res = br.converse(modelId=model_id, body=json.dumps(body))
    out = json.loads(res["body"].read())
    # Normalize text extraction
    parts = out.get("output", {}).get("message", {}).get("content", [])
    text = " ".join([p.get("text","") for p in parts]).strip()
    return text or json.dumps(out)
