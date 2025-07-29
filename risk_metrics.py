import numpy as np

def compute_returns(df):
    return df['Adj Close'].pct_change().dropna()

def compute_volatility(returns):
    return returns.std() * np.sqrt(252)

def compute_sharpe_ratio(returns, risk_free_rate=0.02):
    excess_returns = returns.mean() - risk_free_rate / 252
    return (excess_returns / returns.std()) * np.sqrt(252)

def compute_max_drawdown(df):
    cum_returns = (1 + df['Adj Close'].pct_change().fillna(0)).cumprod()
    peak = cum_returns.cummax()
    drawdown = (cum_returns - peak) / peak
    return drawdown.min()
