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
    
    # Normalize column names to lowercase
    df.columns = df.columns.str.strip().str.lower()
    
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

    # Process each product - OPTIMIZED for speed
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
        
        # Skip LLM explanation for speed - use rule-based reasoning instead
        llm_explanation = None
        
        results["products"].append({
            "product_name": product,
            "forecast": forecast7,
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

    # Skip LLM summary for speed - generate rule-based summary
    high_urgency = [p for p in results["products"] if p["reorder"]["urgency"] == "high"]
    anomaly_products = [p for p in results["products"] if p["anomalies"]]
    low_conf = [p for p in results["products"] if p["confidence_score"] < 60]
    
    if lang == 'en':
        summary = f"Analysis complete: {len(results['products'])} products analyzed. "
        if high_urgency:
            summary += f"{len(high_urgency)} products need urgent reordering. "
        if anomaly_products:
            summary += f"{len(anomaly_products)} products show unusual patterns. "
        if low_conf:
            summary += f"{len(low_conf)} products have low forecast confidence."
    elif lang == 'hi':
        summary = f"विश्लेषण पूर्ण: {len(results['products'])} उत्पादों का विश्लेषण किया गया। "
        if high_urgency:
            summary += f"{len(high_urgency)} उत्पादों को तत्काल पुनः ऑर्डर की आवश्यकता है। "
        if anomaly_products:
            summary += f"{len(anomaly_products)} उत्पाद असामान्य पैटर्न दिखाते हैं। "
    else:  # Marathi
        summary = f"विश्लेषण पूर्ण: {len(results['products'])} उत्पादनांचे विश्लेषण केले. "
        if high_urgency:
            summary += f"{len(high_urgency)} उत्पादनांना तातडीने पुन्हा ऑर्डर आवश्यक आहे। "
        if anomaly_products:
            summary += f"{len(anomaly_products)} उत्पादने असामान्य पॅटर्न दर्शवतात। "

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
