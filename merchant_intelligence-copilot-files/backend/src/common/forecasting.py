import pandas as pd
import numpy as np

def prophet_forecast(df: pd.DataFrame, days=30):
    """
    Prophet-based forecasting with seasonality detection - OPTIMIZED for speed.
    Falls back to moving average if Prophet fails or insufficient data.
    """
    try:
        from prophet import Prophet
        import logging
        
        # Suppress Prophet logging for speed
        logging.getLogger('prophet').setLevel(logging.ERROR)
        logging.getLogger('cmdstanpy').setLevel(logging.ERROR)
        
        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        prophet_df = df.copy()
        prophet_df = prophet_df.rename(columns={"date": "ds", "quantity_sold": "y"})
        prophet_df = prophet_df[["ds", "y"]].sort_values("ds")
        
        # Use moving average for small datasets (< 14 days)
        if len(prophet_df) < 14:
            return moving_average_forecast(df, days)
        
        # For datasets between 14-30 days, use simplified Prophet
        if len(prophet_df) < 30:
            model = Prophet(
                daily_seasonality=False,
                weekly_seasonality=False,  # Disable for small datasets
                yearly_seasonality=False,
                interval_width=0.8,
                changepoint_prior_scale=0.01,  # Less sensitive for small data
                mcmc_samples=0,
                uncertainty_samples=50  # Reduced for speed
            )
        else:
            # Full Prophet for larger datasets
            model = Prophet(
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=False,
                interval_width=0.8,
                changepoint_prior_scale=0.05,
                mcmc_samples=0,
                uncertainty_samples=100
            )
        
        # Fit model with reduced iterations
        model.fit(prophet_df, algorithm='Newton')
        
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
    s = df.sort_values("date").set_index("date")["quantity_sold"]
    
    # Fill missing dates with 0
    s = s.asfreq("D", fill_value=0)
    
    # Calculate moving average (use shorter window for small datasets)
    window = min(7, max(3, len(s) // 3))
    ma = s.rolling(window, min_periods=1).mean()
    base = ma.iloc[-1] if len(ma) > 0 else s.mean()
    
    # Handle case where base is 0 or NaN
    if pd.isna(base) or base == 0:
        base = s.mean() if s.mean() > 0 else 1.0
    
    # Simple weekly seasonality factor from available data
    if len(s) >= 7:
        dow = s.index.dayofweek
        season = s.groupby(dow).mean()
        season_mean = season.mean()
        if season_mean > 0:
            season = season / season_mean
        else:
            season = pd.Series(1.0, index=range(7))
    else:
        # No seasonality for very small datasets
        season = pd.Series(1.0, index=range(7))

    future = []
    last_date = s.index.max()
    for i in range(1, days + 1):
        d = last_date + pd.Timedelta(days=i)
        yhat = float(max(0, base * season.get(d.dayofweek, 1.0)))
        
        # Naive CI band based on historical std
        if len(s) >= 7:
            band = max(1.0, np.std(s.tail(min(28, len(s)))) * 1.5)
        else:
            band = max(1.0, yhat * 0.3)  # 30% band for small datasets
            
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
    
    # Reduce confidence for small datasets
    if len(s) < 14:
        conf = conf * 0.7  # 30% penalty for small datasets
    
    return future, round(conf, 2)
