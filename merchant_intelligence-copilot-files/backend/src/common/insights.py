import pandas as pd
import numpy as np
from scipy import stats

def detect_anomalies(product_df: pd.DataFrame):
    """
    Enhanced anomaly detection using multiple methods:
    - Week-over-week change detection
    - Z-score outlier detection
    - Slow-moving product identification
    """
    s = product_df.sort_values("date")["quantity_sold"]
    if len(s) < 14:
        return []
    
    out = []
    
    # Week-over-week change detection
    last7 = s.tail(7).sum()
    prev7 = s.iloc[-14:-7].sum()
    wow = ((last7 - prev7) / prev7 * 100) if prev7 > 0 else 0
    
    if wow > 30:
        out.append({
            "type": "spike",
            "change_percent": round(wow, 2),
            "severity": "high" if wow > 50 else "medium",
            "description": f"Demand increased {round(wow, 1)}% week-over-week"
        })
    elif wow < -30:
        out.append({
            "type": "drop",
            "change_percent": round(wow, 2),
            "severity": "high" if wow < -50 else "medium",
            "description": f"Demand decreased {abs(round(wow, 1))}% week-over-week"
        })
    
    # Z-score outlier detection (last 7 days vs historical)
    if len(s) >= 28:
        try:
            z_scores = np.abs(stats.zscore(s.tail(28)))
            recent_z = z_scores[-7:].mean()
            if recent_z > 2.5:
                out.append({
                    "type": "outlier",
                    "z_score": round(recent_z, 2),
                    "severity": "high" if recent_z > 3 else "medium",
                    "description": f"Recent sales pattern is unusual (Z-score: {round(recent_z, 2)})"
                })
        except Exception:
            pass  # Skip if Z-score calculation fails
    
    # Slow-moving product detection
    avg = s.mean()
    if last7 < 0.5 * avg * 7 and avg > 0:
        out.append({
            "type": "slow_moving",
            "current_velocity": round(last7 / 7, 2),
            "avg_velocity": round(avg, 2),
            "severity": "medium",
            "description": f"Sales velocity dropped to {round((last7/7)/avg*100, 1)}% of average"
        })
    
    return out


def reorder_recommendation(forecast7, safety=0.2, current_stock=None):
    """
    Calculate reorder quantity based on forecast and safety stock.
    Includes urgency level based on stockout risk.
    """
    demand = sum([d["yhat"] for d in forecast7])
    qty = demand * (1 + safety)
    
    # Determine urgency based on quantity and current stock
    if current_stock is not None:
        days_of_stock = current_stock / (demand / 7) if demand > 0 else 999
        if days_of_stock < 3:
            urgency = "high"
        elif days_of_stock < 7:
            urgency = "medium"
        else:
            urgency = "low"
    else:
        # Fallback: urgency based on quantity
        urgency = "high" if qty > 100 else "medium" if qty > 50 else "low"
    
    return round(qty, 2), urgency


def simple_price_hint(product_df: pd.DataFrame):
    """
    Price optimization suggestions based on demand trends and elasticity.
    """
    s = product_df.sort_values("date")["quantity_sold"]
    if len(s) < 14:
        return None
    
    last7 = s.tail(7).sum()
    prev7 = s.iloc[-14:-7].sum()
    price = product_df["price"].median()
    
    if prev7 <= 0:
        return None
    
    change = (last7 - prev7) / prev7
    
    if change > 0.2:
        return {
            "action": "increase",
            "suggested_delta": round(price * 0.03, 2),
            "reason": "Demand trending up (WoW>20%). Price increase unlikely to hurt sales.",
            "expected_impact": f"+{round(price * 0.03 * last7, 2)} revenue"
        }
    elif change < -0.2:
        return {
            "action": "discount",
            "suggested_delta": round(price * 0.05, 2),
            "reason": "Demand trending down (WoW<-20%). Discount may stimulate sales.",
            "expected_impact": f"Potential to recover {round(abs(change) * 50, 1)}% of lost volume"
        }
    else:
        return {
            "action": "hold",
            "suggested_delta": 0,
            "reason": "Demand stable. Current pricing is optimal.",
            "expected_impact": "Maintain current revenue"
        }


def generate_demand_reasoning(product_df: pd.DataFrame, forecast, anomalies):
    """
    Generate plain-language explanation for demand patterns.
    This can be enhanced with LLM but provides rule-based baseline.
    """
    s = product_df.sort_values("date")["quantity_sold"]
    
    # Trend analysis
    recent_avg = s.tail(7).mean()
    historical_avg = s.mean()
    trend = "increasing" if recent_avg > historical_avg * 1.1 else "decreasing" if recent_avg < historical_avg * 0.9 else "stable"
    
    # Seasonality detection
    if len(s) >= 28:
        dow_pattern = s.groupby(s.index.dayofweek).mean()
        has_weekly_pattern = dow_pattern.std() / dow_pattern.mean() > 0.3 if dow_pattern.mean() > 0 else False
    else:
        has_weekly_pattern = False
    
    reasoning = f"Demand is {trend}. "
    
    if has_weekly_pattern:
        reasoning += "Weekly seasonality detected. "
    
    if anomalies:
        reasoning += f"{len(anomalies)} anomalies detected: {', '.join([a['type'] for a in anomalies])}. "
    
    # Forecast summary
    forecast_avg = np.mean([f["yhat"] for f in forecast])
    if forecast_avg > recent_avg * 1.1:
        reasoning += "Forecast predicts demand increase."
    elif forecast_avg < recent_avg * 0.9:
        reasoning += "Forecast predicts demand decrease."
    else:
        reasoning += "Forecast predicts stable demand."
    
    return reasoning
