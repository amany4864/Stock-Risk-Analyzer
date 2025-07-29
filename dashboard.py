# dashboard.py

import streamlit as st
from utils import fetch_stock_data
from risk_metrics import compute_returns, compute_volatility, compute_sharpe_ratio, compute_max_drawdown
from visualizer import plot_price, plot_returns
from report_generator import create_pdf_report
import datetime
import base64

st.set_page_config(page_title="Risk Analytics Dashboard", layout="wide")
st.title("📊 Risk Analytics Dashboard")

# Sidebar Inputs
st.sidebar.header("Input Parameters")
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=datetime.date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", value=datetime.date(2024, 1, 1))

if st.sidebar.button("Run Analysis"):
    df = fetch_stock_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

    if df is None or df.empty:
        st.error("❌ No data found. Please check the ticker or date range.")
    else:
        st.success(f"✅ Data loaded for {ticker} from {start_date} to {end_date}")

        # Compute risk metrics
        returns = compute_returns(df)
        volatility = compute_volatility(returns)
        sharpe = compute_sharpe_ratio(returns)
        drawdown = compute_max_drawdown(df)

        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Volatility", f"{volatility:.4f}")
        col2.metric("Sharpe Ratio", f"{sharpe:.4f}")
        col3.metric("Max Drawdown", f"{drawdown * 100:.2f}%")

        # Generate plots and save images
        st.subheader("📈 Price Chart")
        price_fig, price_path = plot_price(df, ticker)
        st.pyplot(price_fig)

        st.subheader("📉 Returns Chart")
        return_fig, return_path = plot_returns(returns, ticker)
        st.pyplot(return_fig)

        # Prepare context for report
        context = {
            "ticker": ticker,
            "volatility": round(volatility, 4),
            "sharpe_ratio": round(sharpe, 4),
            "max_drawdown": round(drawdown * 100, 2),
            "price_plot": price_path,
            "return_plot": return_path
        }

        # Generate and download PDF
        