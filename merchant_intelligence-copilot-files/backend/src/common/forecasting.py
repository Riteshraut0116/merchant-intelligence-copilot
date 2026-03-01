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
    Works with as little as 3 days of data.
    """
    # df columns: date, quantity_sold
    s = df.sort_values("date").set_index("date")["quantity_sold"].asfreq("D").fillna(0)
    
    if len(s) == 0:
        # Return zero forecast if no data
        future = []
        last_date = pd.Timestamp.now()
        for i in range(1, days + 1):
            d = last_date + pd.Timedelta(days=i)
            future.append({
                "ds": d.date().isoformat(),
                "yhat": 0,
                "yhat_lower": 0,
                "yhat_upper": 0
            })
        return future, 50
    
    # Calculate moving average (use smaller window for small datasets)
    window = min(7, max(3, len(s) // 2))
    ma = s.rolling(window, min_periods=1).mean().fillna(s.mean())
    base = ma.iloc[-1] if len(ma) > 0 else s.mean()
    
    # Simple weekly seasonality factor (only if we have enough data)
    if len(s) >= 7:
        dow = s.index.dayofweek
        season = s.groupby(dow).mean()
        season_mean = season.mean() if season.mean() != 0 else 1.0
        season = season / season_mean
    else:
        # No seasonality for very small datasets
        season = pd.Series([1.0] * 7, index=range(7))

    future = []
    last_date = s.index.max()
    for i in range(1, days + 1):
        d = last_date + pd.Timedelta(days=i)
        yhat = float(max(0, base * season.get(d.dayofweek, 1.0)))
        # Naive CI band based on recent volatility
        if len(s) >= 7:
            band = max(1.0, np.std(s.tail(min(28, len(s)))) * 1.5)
        else:
            band = yhat * 0.3  # 30% band for small datasets
        future.append({
            "ds": d.date().isoformat(),
            "yhat": round(yhat, 2),
            "yhat_lower": round(max(0, yhat - band), 2),
            "yhat_upper": round(yhat + band, 2)
        })
    
    # Confidence score: narrower band => higher confidence
    # Lower confidence for smaller datasets
    widths = [f["yhat_upper"] - f["yhat_lower"] for f in future]
    avg_pred = np.mean([f["yhat"] for f in future]) or 1.0
    base_conf = max(0, min(100, 100 - (np.mean(widths) / avg_pred * 100)))
    
    # Reduce confidence based on data size
    data_penalty = max(0, (14 - len(s)) * 3)  # Lose 3% per day below 14 days
    conf = max(30, base_conf - data_penalty)  # Minimum 30% confidence
    
    return future, round(conf, 2)
