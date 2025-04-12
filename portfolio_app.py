import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Ghana Portfolio Analysis", layout="centered")

st.title("📊 Ghana Stock Portfolio Analysis")

uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Load Excel using openpyxl
        df = pd.read_excel(uploaded_file, engine='openpyxl', index_col=0, parse_dates=True)
        df = df.fillna(method='ffill')  # Forward-fill missing values
        st.success("✅ File loaded successfully")
        st.dataframe(df.head())

        # === Portfolio Config ===
        weights = np.array([0.4, 0.3, 0.3])  # Adjust to match your stocks
        risk_free_rate = 0.03 / 252

        # === Calculations ===
        returns = df.pct_change().dropna()
        mean_returns = returns.mean()
        cov_matrix = returns.cov()

        daily_return = np.dot(mean_returns, weights)
        annual_return = daily_return * 252
        variance = np.dot(weights.T, np.dot(cov_matrix, weights)) * 252
        std_dev = np.sqrt(variance)
        sharpe = (annual_return - 0.03) / std_dev

        st.subheader("📈 Portfolio Metrics")
        st.markdown(f"**Expected Annual Return:** {annual_return:.2%}")
        st.markdown(f"**Portfolio Variance:** {variance:.6f}")
        st.markdown(f"**Standard Deviation:** {std_dev:.2%}")
        st.markdown(f"**Sharpe Ratio:** {sharpe:.4f}")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("Please upload an Excel file.")
