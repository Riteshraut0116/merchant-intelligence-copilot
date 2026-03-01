import pandas as pd
import numpy as np

def prophet_forecast(df: pd.DataFrame, days=30):
    """
    Forecasting with moving average and seasonality detection.
    Optimized for Render deployment (no Prophet dependency).
    """
    # Use moving average forecast (Prophet removed for deployment compatibility)
    return moving_average_forecast(df, days)


def moving_average_forecast(df: pd.DataFrame, days=30):
    """
    Simple moving average forecast with weekly seasonality.
    Lightweight and fast - no heavy dependencies required.
    """
    # df columns: date, quantity_sold
    s = df.sort_values("date").set_index("date")["quantity_sold"].asfreq("D").fillna(0)
    
    # Calculate 7-day moving average
    ma7 = s.rolling(7, min_periods=1).mean().fillna(s.mean())
    base = ma7.iloc[-1] if len(ma7) > 0 else s.mean()
    
    # Simple weekly seasonality factor from last 4 weeks
    dow = s.index.dayofweek
    season = s.groupby(dow).mean()
    season_mean = season.mean() if season.mean() != 0 else 1.0
    season = season / season_mean

    future = []
    last_date = s.index.max()
    for i in range(1, days + 1):
        d = last_date + pd.Timedelta(days=i)
        yhat = float(max(0, base * season.get(d.dayofweek, 1.0)))
        # Naive CI band based on recent volatility
        band = max(1.0, np.std(s.tail(28)) * 1.5) if len(s) >= 28 else yhat * 0.3
        future.append({
            "ds": d.date().isoformat(),
            "yhat": round(yhat, 2),
            "yhat_lower": round(max(0, yhat - band), 2),
            "yhat_upper": round(yhat + band, 2)
        })
    
    # Confidence score: narrower band => higher confidence
    widths = [f["yhat_upper"] - f["yhat_lower"] for f in future]
    avg_pred = np.mean([f["yhat"] for f in future]) or 1.0
    conf = max(0, min(100, 100 - (np.mean(widths) / avg_pred * 100)))
    
    return future, round(conf, 2)
