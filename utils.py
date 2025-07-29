import yfinance as yf
import pandas as pd
import numpy as np

def fetch_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Fetch stock data for a single ticker with fallback for Adj Close / Close.
    Handles MultiIndex if returned from yfinance.
    """
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)

    if df is None or df.empty:
        raise ValueError("No data fetched. Check ticker or connection.")

    # Flatten MultiIndex if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [f"{col[0]} {col[1]}" if col[1] else col[0] for col in df.columns]

    print("Downloaded Columns:", df.columns.tolist())  # Debug

    # Try to get 'Adj Close' or fallback to 'Close'
    adj_close_col = next(
        (col for col in df.columns if 'adj close' in col.lower()),
        None
    )
    if not adj_close_col:
        adj_close_col = next(
            (col for col in df.columns if col.lower().startswith('close')),
            None
        )

    if not adj_close_col:
        raise KeyError("Could not find 'Adj Close' or 'Close' column")

    # Extract, clean, and rename column
    df = df[[adj_close_col]].copy()
    df.dropna(inplace=True)
    df.rename(columns={adj_close_col: 'Adj Close'}, inplace=True)
    return df
