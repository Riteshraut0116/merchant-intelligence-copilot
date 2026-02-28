import json, io
import pandas as pd
import numpy as np
from common.responses import ok, bad
from common.validators import validate_csv_columns
from common.forecasting import prophet_forecast
from common.insights import detect_anomalies, reorder_recommendation, simple_price_hint, generate_demand_reasoning
from common.config import BEDROCK_MODEL_FAST
from common.bedrock_nova import nova_converse

DISCLAIMER = "AI‑assisted insights to support smarter business decisions."

def lambda_handler(event, context):
    try:
        payload = json.loads(event.get("body") or "{}")
    except Exception:
        return bad("Invalid JSON body")

    csv_text = payload.get("csv_text")
    if not csv_text:
        return bad("Provide csv_text in request body for prototype demo")

    # Parse and validate CSV
    try:
        df = pd.read_csv(io.StringIO(csv_text))
    except Exception as e:
        return bad(f"Failed to parse CSV: {str(e)}")
    
    missing = validate_csv_columns(df.columns)
    if missing:
        return bad("Missing required columns", {"missing_columns": missing})

    # Data cleaning and preprocessing
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "product_name"])
    df["product_name"] = df["product_name"].astype(str).str.strip().str.title()
    
    for c in ["quantity_sold", "price", "revenue"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    
    # Remove outliers using Z-score (threshold > 3)
    from scipy import stats
    for col in ["quantity_sold", "price"]:
        z_scores = np.abs(stats.zscore(df[col]))
        df = df[z_scores < 3]

    results = {"products": [], "disclaimer": DISCLAIMER}
    lang = payload.get("language", "en")

    # Process each product
    for product in sorted(df["product_name"].unique()):
        p = df[df["product_name"] == product].copy()
        daily = p.groupby("date", as_index=False)["quantity_sold"].sum()
        
        # Skip products with insufficient data
        if len(daily) < 14:
            continue
        
        # Generate forecast using Prophet (with moving average fallback)
        forecast30, conf = prophet_forecast(
            daily.rename(columns={"date": "date", "quantity_sold": "quantity_sold"}),
            days=30
        )
        forecast7 = forecast30[:7]
        
        # Detect anomalies
        anomalies = detect_anomalies(p)
        
        # Generate reorder recommendation
        reorder_qty, urgency = reorder_recommendation(forecast7)
        
        # Price optimization hint
        price_hint = simple_price_hint(p)
        
        # Generate demand reasoning (rule-based baseline)
        demand_reasoning = generate_demand_reasoning(p, forecast7, anomalies)
        
        # LLM-powered explainability for high-value insights
        try:
            if conf < 70 or len(anomalies) > 0 or urgency == "high":
                system = f"You are a business advisor for Indian MSME merchants. Explain insights in {lang}. Be concise and actionable."
                user = f"""Product: {product}
Forecast confidence: {conf}%
Anomalies: {json.dumps(anomalies)}
Reorder: {reorder_qty} units ({urgency} urgency)
Price hint: {json.dumps(price_hint)}

Explain in 2-3 sentences why this product needs attention and what action to take."""
                
                llm_explanation = nova_converse(BEDROCK_MODEL_FAST, system, user)
            else:
                llm_explanation = None
        except Exception as e:
            llm_explanation = None
            print(f"LLM explanation failed: {e}")
        
        results["products"].append({
            "product_name": product,
            "forecast": forecast7,  # Changed from forecast_7d to match frontend
            "forecast_30d": forecast30,
            "confidence_score": conf,
            "anomalies": anomalies,
            "reorder": {"quantity": reorder_qty, "urgency": urgency},
            "price_hint": price_hint,
            "demand_reasoning": demand_reasoning,
            "llm_explanation": llm_explanation,
            "reorder_logic": f"Recommended quantity: {reorder_qty} units. Based on 7-day forecast ({sum([f['yhat'] for f in forecast7]):.1f} units) plus 20% safety stock.",
            "confidence_explanation": f"Confidence score of {conf}% based on forecast accuracy, data quality ({len(daily)} days of history), and prediction interval width."
        })

    # Generate overall summary with LLM
    system = f"You are a business advisor for Indian MSME merchants. Respond in {lang}. Be concise, actionable, and avoid jargon."
    user = f"""Summarize the key actions for this merchant from the following insights.
Return:
1) Top 3 priorities (be specific about products)
2) 1-line reason for each priority
3) Mention any critical anomalies or low confidence items

Insights JSON: {json.dumps(results['products'][:8], ensure_ascii=False)}
"""
    
    try:
        summary = nova_converse(BEDROCK_MODEL_FAST, system, user)
    except Exception as e:
        summary = f"Summary unavailable (Bedrock error). Use dashboard insights directly. ({str(e)})"

    # Data quality report
    quality_report = {
        "total_products": len(results["products"]),
        "date_range": f"{df['date'].min().date()} to {df['date'].max().date()}",
        "total_records": len(df),
        "avg_confidence": round(sum([p["confidence_score"] for p in results["products"]]) / len(results["products"]), 2) if results["products"] else 0,
        "high_urgency_count": len([p for p in results["products"] if p["reorder"]["urgency"] == "high"]),
        "anomaly_count": len([p for p in results["products"] if p["anomalies"]])
    }

    return ok({
        "insights": results,
        "summary": summary,
        "quality_report": quality_report,
        "disclaimer": DISCLAIMER
    })
