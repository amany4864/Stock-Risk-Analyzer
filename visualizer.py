# visualizer.py

import matplotlib.pyplot as plt
import os
import tempfile

def plot_price(df, ticker):
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Use 'Adj Close' if available
    if 'Adj Close' in df.columns:
        df['Adj Close'].plot(ax=ax, title=f"{ticker} Price Chart")
        ax.set_ylabel("Price (Adj Close)")
    elif 'Close' in df.columns:
        df['Close'].plot(ax=ax, title=f"{ticker} Price Chart")
        ax.set_ylabel("Price (Close)")
    else:
        raise KeyError("DataFrame must contain 'Adj Close' or 'Close' column.")

    ax.grid(True)

    # Save image
    tmp_dir = tempfile.gettempdir()
    image_path = os.path.join(tmp_dir, f"{ticker}_price.png")
    fig.savefig(image_path, bbox_inches='tight')
    return fig, image_path


def plot_returns(returns, ticker):
    fig, ax = plt.subplots(figsize=(10, 4))
    returns.plot(ax=ax, title=f"{ticker} Daily Returns")
    ax.set_ylabel("Returns")
    ax.grid(True)

    # Save image
    tmp_dir = tempfile.gettempdir()
    image_path = os.path.join(tmp_dir, f"{ticker}_returns.png")
    fig.savefig(image_path, bbox_inches='tight')
    return fig, image_path
