import yfinance as yf
import pandas as pd
import statsmodels.api as sm

def run_impact_model(ticker, event_date, benchmark='^IXIC', est_window=252, event_window=3):
    """
    Runs an OLS regression to calculate Cumulative Abnormal Returns (CAR) 
    around a specific corporate event.
    """
    # 1. Define timeframes
    event_dt = pd.to_datetime(event_date)
    start_date = event_dt - pd.Timedelta(days=est_window + 50)
    end_date = event_dt + pd.Timedelta(days=event_window + 10)
    
    # 2. Fetch daily close prices separately to avoid yfinance formatting bugs
    stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    market_data = yf.download(benchmark, start=start_date, end=end_date, progress=False)
    
    # Safety check: If the stock was delisted (like SMAR), abort cleanly
    if stock_data.empty:
        raise ValueError(f"No market data found. The stock may be delisted.")
        
    # Combine into one clean DataFrame using 'Close' prices
    data = pd.DataFrame({
        'Stock': stock_data['Close'].squeeze(),
        'Market': market_data['Close'].squeeze()
    }).dropna()
    
    returns = data.pct_change().dropna()
    
    # 3. Split data into Estimation Window and Event Window
    estimation_data = returns.loc[:event_dt - pd.Timedelta(days=event_window + 1)].tail(est_window)
    event_data = returns.loc[event_dt - pd.Timedelta(days=event_window) : event_dt + pd.Timedelta(days=event_window)]
    
    # 4. Fit the OLS Regression Model on the estimation period
    X_est = sm.add_constant(estimation_data['Market'])
    y_est = estimation_data['Stock']
    model = sm.OLS(y_est, X_est).fit()
    
    # 5. Calculate Abnormal Returns during the event window
    X_event = sm.add_constant(event_data['Market'])
    expected_returns = model.predict(X_event)
    abnormal_returns = event_data['Stock'] - expected_returns
    
    car = abnormal_returns.sum()
    
    return {
        "Ticker": ticker,
        "Alpha": model.params['const'],
        "Beta": model.params['Market'],
        "CAR": car,
        "Abnormal_Returns": abnormal_returns
    }