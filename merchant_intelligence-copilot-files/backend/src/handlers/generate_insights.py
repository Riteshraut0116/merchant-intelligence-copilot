import json, io
import pandas as pd
from common.responses import ok, bad
from common.validators import validate_csv_columns
from common.forecasting import moving_average_forecast
from common.insights import detect_anomalies, reorder_recommendation, simple_price_hint
from common.config import BEDROCK_MODEL_FAST
from common.bedrock_nova import nova_converse

DISCLAIMER = "AI‑assisted insights to support smarter business decisions."

def lambda_handler(event, context):
    try:
        payload = json.loads(event.get("body") or "{}")
    except Exception:
        return bad("Invalid JSON body")

    csv_text = payload.get("csv_text")  # simplest for prototype
    if not csv_text:
        return bad("Provide csv_text in request body for prototype demo")

    df = pd.read_csv(io.StringIO(csv_text))
    missing = validate_csv_columns(df.columns)
    if missing:
        return bad("Missing required columns", {"missing_columns": missing})

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date","product_name"])
    df["product_name"] = df["product_name"].astype(str).str.strip()
    for c in ["quantity_sold","price","revenue"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    results = {"products":[], "disclaimer": DISCLAIMER}
    lang = payload.get("language","en")

    for product in sorted(df["product_name"].unique()):
        p = df[df["product_name"]==product].copy()
        daily = p.groupby("date", as_index=False)["quantity_sold"].sum()
        if len(daily) < 14:
            continue
        forecast30, conf = moving_average_forecast(daily.rename(columns={"date":"date","quantity_sold":"quantity_sold"}), days=30)
        forecast7 = forecast30[:7]
        anomalies = detect_anomalies(p)
        reorder_qty, urgency = reorder_recommendation(forecast7)

        price_hint = simple_price_hint(p)

        results["products"].append({
            "product_name": product,
            "forecast_7d": forecast7,
            "forecast_30d": forecast30,
            "confidence_score": conf,
            "anomalies": anomalies,
            "reorder": {"quantity": reorder_qty, "urgency": urgency},
            "price_hint": price_hint
        })

    # LLM summary
    system = f"You are a business advisor for Indian MSME merchants. Respond in {lang}. Be concise, actionable, and avoid jargon."
    user = f"""Summarize the key actions for this merchant from the following insights.
Return:
1) Top 3 priorities
2) 1-line reason each
3) Mention confidence and any anomalies
Insights JSON: {json.dumps(results['products'][:8], ensure_ascii=False)}
"""
    try:
        summary = nova_converse(BEDROCK_MODEL_FAST, system, user)
    except Exception as e:
        summary = f"Summary unavailable (Bedrock error). Use dashboard insights directly. ({str(e)})"

    return ok({"insights": results, "summary": summary, "disclaimer": DISCLAIMER})
