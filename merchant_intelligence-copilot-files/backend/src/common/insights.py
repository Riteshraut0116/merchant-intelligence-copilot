import pandas as pd
import numpy as np

def detect_anomalies(product_df: pd.DataFrame):
    # expects sorted by date
    s = product_df.sort_values("date")["quantity_sold"]
    if len(s) < 14:
        return []
    last7 = s.tail(7).sum()
    prev7 = s.iloc[-14:-7].sum()
    wow = ((last7 - prev7)/prev7*100) if prev7>0 else 0
    out=[]
    if wow > 30:
        out.append({"type":"spike","change_percent":round(wow,2),"severity":"high" if wow>50 else "medium"})
    elif wow < -30:
        out.append({"type":"drop","change_percent":round(wow,2),"severity":"high" if wow<-50 else "medium"})

    avg = s.mean()
    if last7 < 0.5 * avg * 7:
        out.append({"type":"slow_moving","current_velocity":round(last7/7,2),"avg_velocity":round(avg,2),"severity":"medium"})
    return out

def reorder_recommendation(forecast7, safety=0.2):
    demand = sum([d["yhat"] for d in forecast7])
    qty = demand * (1+safety)
    urgency = "high" if qty>100 else "medium"
    return round(qty,2), urgency

def simple_price_hint(product_df: pd.DataFrame):
    # heuristic: if demand rising (last7 > prev7), suggest slight price increase, else discount
    s = product_df.sort_values("date")["quantity_sold"]
    if len(s) < 14:
        return None
    last7 = s.tail(7).sum()
    prev7 = s.iloc[-14:-7].sum()
    price = product_df["price"].median()
    if prev7<=0: return None
    change = (last7-prev7)/prev7
    if change>0.2:
        return {"action":"increase","suggested_delta": round(price*0.03,2), "reason":"Demand trending up (WoW>20%)"}
    if change<-0.2:
        return {"action":"discount","suggested_delta": round(price*0.05,2), "reason":"Demand trending down (WoW<-20%)"}
    return {"action":"hold","suggested_delta": 0, "reason":"Demand stable"}
