import json
from datetime import datetime
from common.responses import ok, bad
from common.config import BEDROCK_MODEL_FAST
from common.bedrock_nova import nova_converse

def lambda_handler(event, context):
    """
    Generate weekly action plan report using LLM.
    Expects insights data in request body or retrieves from storage.
    """
    try:
        payload = json.loads(event.get("body") or "{}")
    except Exception:
        return bad("Invalid JSON body")
    
    # Get insights data (from request or storage)
    insights_data = payload.get("insights")
    lang = payload.get("language", "en")
    
    if not insights_data or not insights_data.get("products"):
        return bad("No insights data available. Please generate insights first.")
    
    products = insights_data.get("products", [])
    
    # Analyze products for report generation
    high_urgency = [p for p in products if p.get("reorder", {}).get("urgency") == "high"]
    anomalies = [p for p in products if p.get("anomalies") and len(p["anomalies"]) > 0]
    low_confidence = [p for p in products if p.get("confidence_score", 100) < 60]
    price_opportunities = [p for p in products if p.get("price_hint", {}).get("action") in ["increase", "discount"]]
    
    # Prepare context for LLM
    context = {
        "total_products": len(products),
        "high_urgency_reorders": len(high_urgency),
        "anomaly_products": len(anomalies),
        "low_confidence_products": len(low_confidence),
        "price_optimization_opportunities": len(price_opportunities),
        "top_reorders": [{"name": p["product_name"], "qty": p["reorder"]["quantity"]} for p in high_urgency[:5]],
        "top_anomalies": [{"name": p["product_name"], "anomalies": p["anomalies"]} for p in anomalies[:5]],
        "price_actions": [{"name": p["product_name"], "action": p["price_hint"]["action"], "reason": p["price_hint"]["reason"]} for p in price_opportunities[:3]]
    }
    
    # Generate weekly report with LLM
    system = f"""You are a business advisor for Indian MSME merchants. Generate a weekly action plan in {lang}.
Be specific, actionable, and prioritize by business impact. Use simple language."""
    
    user = f"""Generate a weekly action plan based on these insights:

Context:
- Total products analyzed: {context['total_products']}
- High urgency reorders needed: {context['high_urgency_reorders']}
- Products with anomalies: {context['anomaly_products']}
- Low confidence forecasts: {context['low_confidence_products']}
- Price optimization opportunities: {context['price_optimization_opportunities']}

Top Reorder Priorities:
{json.dumps(context['top_reorders'], indent=2)}

Anomalies Detected:
{json.dumps(context['top_anomalies'], indent=2)}

Price Optimization:
{json.dumps(context['price_actions'], indent=2)}

Generate a structured report with:
1. Top 3 Priorities (specific products and actions)
2. Expected business impact for each priority
3. Risks and alerts to watch
4. Quick wins for this week

Format as JSON with keys: priorities (array of {{title, description, impact}}), risks (array of strings), quick_wins (array of strings)"""
    
    try:
        llm_response = nova_converse(BEDROCK_MODEL_FAST, system, user)
        
        # Try to parse as JSON, fallback to structured text
        try:
            report_data = json.loads(llm_response)
        except:
            # If LLM doesn't return valid JSON, create structured report
            report_data = {
                "priorities": [
                    {
                        "title": "High Priority Reorders",
                        "description": f"{len(high_urgency)} products need urgent reordering: {', '.join([p['product_name'] for p in high_urgency[:3]])}",
                        "impact": "Prevent stockouts and maintain sales"
                    },
                    {
                        "title": "Address Demand Anomalies",
                        "description": f"{len(anomalies)} products showing unusual patterns: {', '.join([p['product_name'] for p in anomalies[:3]])}",
                        "impact": "Adjust inventory and pricing strategy"
                    },
                    {
                        "title": "Price Optimization",
                        "description": f"{len(price_opportunities)} products have pricing opportunities",
                        "impact": "Increase revenue through strategic pricing"
                    }
                ],
                "risks": [
                    f"{len(high_urgency)} products at risk of stockout" if len(high_urgency) > 3 else None,
                    f"{len(anomalies)} products with unusual demand patterns" if len(anomalies) > 2 else None,
                    f"{len(low_confidence)} products with low forecast confidence" if len(low_confidence) > 0 else None
                ],
                "quick_wins": [
                    f"Order {high_urgency[0]['product_name']} immediately" if high_urgency else None,
                    f"Adjust price for {price_opportunities[0]['product_name']}" if price_opportunities else None,
                    "Review low confidence items for data quality"
                ]
            }
            # Remove None values
            report_data["risks"] = [r for r in report_data["risks"] if r]
            report_data["quick_wins"] = [q for q in report_data["quick_wins"] if q]
        
        # Add metadata
        report_data["generated_at"] = datetime.utcnow().isoformat()
        report_data["language"] = lang
        report_data["summary_text"] = llm_response if isinstance(llm_response, str) else None
        
        return ok({
            "report": report_data,
            "context": context,
            "disclaimer": "AI-generated action plan. Review with your business knowledge before implementing."
        })
        
    except Exception as e:
        return bad(f"Failed to generate report: {str(e)}")
