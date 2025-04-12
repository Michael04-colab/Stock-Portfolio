# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16SHdYp-Vhv0lTByo4u4L4WCPsn5cKrgt
"""

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Portfolio Analysis Tool", layout="centered")

st.title("📈 Ghana Stock Portfolio Analysis")
st.write("Upload your Excel sheet with historical stock prices (each column is a stock, rows are daily prices).")

# === Upload File ===
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        sheet_name = st.text_input("Sheet name", value="Prices")
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name, index_col=0, engine='openpyxl', parse_dates=True)
        df = df.sort_index()
        df = df.fillna(method='ffill').dropna()

        st.write("✅ Data Preview", df.tail())

        # === Input weights ===
        stocks = df.columns.tolist()
        st.write("Detected Stocks:", stocks)
        weights_input = st.text_input(f"Enter portfolio weights for {len(stocks)} stocks (comma-separated)", "0.4,0.3,0.3")
        weights = np.array([float(w.strip()) for w in weights_input.split(",")])

        if len(weights) != len(stocks):
            st.error("Number of weights must match number of stocks.")
        else:
            weights = weights / np.sum(weights)  # normalize if not 1
            returns = df.pct_change().dropna()
            mean_daily_returns = returns.mean()
            cov_matrix = returns.cov()

            portfolio_daily_return = np.dot(mean_daily_returns, weights)
            portfolio_annual_return = portfolio_daily_return * 252
            portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights)) * 252
            portfolio_std_dev = np.sqrt(portfolio_variance)
            sharpe_ratio = (portfolio_annual_return - 0.03) / portfolio_std_dev

            st.subheader("📊 Portfolio Metrics")
            st.metric("Expected Annual Return", f"{portfolio_annual_return:.2%}")
            st.metric("Portfolio Variance", f"{portfolio_variance:.6f}")
            st.metric("Standard Deviation", f"{portfolio_std_dev:.2%}")
            st.metric("Sharpe Ratio", f"{sharpe_ratio:.4f}")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
