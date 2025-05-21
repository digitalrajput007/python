import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objs as go

st.set_page_config(page_title="Stock Signal Dashboard", layout="wide")

st.title("📈 Stock Signal Dashboard")

symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")
df = yf.download(symbol, period="6mo", interval="1d")

if not df.empty:
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['SMA50'] = ta.sma(df['Close'], length=50)
    df['SMA200'] = ta.sma(df['Close'], length=200)

    st.subheader(f"Price & Indicators for {symbol}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Close"))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'], name="SMA 50"))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA200'], name="SMA 200"))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Signal Suggestions:")
    latest_rsi = df['RSI'].dropna().iloc[-1]
    st.write(f"**RSI**: {latest_rsi:.2f}")

    if latest_rsi < 30:
        st.success("Buy Signal (RSI < 30)")
    elif latest_rsi > 70:
        st.error("Sell Signal (RSI > 70)")
    else:
        st.info("Neutral")

else:
    st.warning("Invalid symbol or no data.")
