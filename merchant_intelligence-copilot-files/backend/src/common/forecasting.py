import pandas as pd
import numpy as np

def prophet_forecast(df: pd.DataFrame, days=30):
    """
    Prophet-based forecasting with seasonality detection.
    Falls back to moving average if Prophet fails or insufficient data.
    """
    try:
        from prophet import Prophet
        
        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        prophet_df = df.copy()
        prophet_df = prophet_df.rename(columns={"date": "ds", "quantity_sold": "y"})
        prophet_df = prophet_df[["ds", "y"]].sort_values("ds")
        
        # Need at least 30 days for Prophet
        if len(prophet_df) < 30:
            return moving_average_forecast(df, days)
        
        # Initialize Prophet with daily and weekly seasonality
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=len(prophet_df) >= 365,
            interval_width=0.8,
            changepoint_prior_scale=0.05
        )
        
        # Fit model
        model.fit(prophet_df)
        
        # Generate future dates
        future = model.make_future_dataframe(periods=days, freq='D')
        forecast = model.predict(future)
        
        # Extract forecast for future dates only
        forecast_future = forecast.tail(days)
        
        # Format output
        results = []
        for _, row in forecast_future.iterrows():
            results.append({
                "ds": row["ds"].date().isoformat(),
                "yhat": round(max(0, row["yhat"]), 2),
                "yhat_lower": round(max(0, row["yhat_lower"]), 2),
                "yhat_upper": round(max(0, row["yhat_upper"]), 2)
            })
        
        # Calculate confidence score based on prediction interval width
        widths = [r["yhat_upper"] - r["yhat_lower"] for r in results]
        avg_pred = np.mean([r["yhat"] for r in results]) or 1.0
        conf = max(0, min(100, 100 - (np.mean(widths) / avg_pred * 50)))
        
        return results, round(conf, 2)
        
    except Exception as e:
        # Fallback to moving average if Prophet fails
        print(f"Prophet forecast failed: {e}. Using moving average fallback.")
        return moving_average_forecast(df, days)


def moving_average_forecast(df: pd.DataFrame, days=30):
    """
    Simple moving average forecast with weekly seasonality.
    Used as fallback when Prophet is unavailable or fails.
    """
    # df columns: date, quantity_sold
    s = df.sort_values("date").set_index("date")["quantity_sold"].asfreq("D").fillna(0)
    ma7 = s.rolling(7).mean().fillna(s.mean())
    base = ma7.iloc[-1]
    
    # Simple weekly seasonality factor from last 4 weeks
    dow = s.index.dayofweek
    season = s.groupby(dow).mean()
    season = season / (season.mean() if season.mean() != 0 else 1.0)

    future = []
    last_date = s.index.max()
    for i in range(1, days + 1):
        d = last_date + pd.Timedelta(days=i)
        yhat = float(max(0, base * season.get(d.dayofweek, 1.0)))
        # Naive CI band
        band = max(1.0, np.std(s.tail(28)) * 1.5)
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
