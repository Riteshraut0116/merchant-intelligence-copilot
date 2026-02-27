import json

def resp(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Merchant-Id",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        },
        "body": json.dumps(body, ensure_ascii=False)
    }

def ok(body): return resp(200, body)
def bad(msg, extra=None):
    b={"error":"BadRequest","message":msg}
    if extra: b["details"]=extra
    return resp(400,b)
