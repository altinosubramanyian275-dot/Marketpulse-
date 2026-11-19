
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="MarketPulse",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: white;
}
h1 {
    color: #00d4aa;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 MARKETPULSE")
st.subheader("Multi-Market Analysis Dashboard")
st.caption("Educational paper-trading mode")

markets = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "BTC/USD": "BTC-USD"
}

def analyse_market(data):
    data = data.copy()

    data["EMA20"] = data["Close"].ewm(
        span=20, adjust=False
    ).mean()

    data["EMA50"] = data["Close"].ewm(
        span=50, adjust=False
    ).mean()

    change = data["Close"].diff()
    gains = change.clip(lower=0)
    losses = -change.clip(upper=0)

    avg_gain = gains.rolling(14).mean()
    avg_loss = losses.rolling(14).mean()

    rs = avg_gain / avg_loss.replace(0, float("nan"))
    data["RSI"] = 100 - (100 / (1 + rs))

    return data

def get_signal(data):
    if data.empty or len(data) < 50:
        return "INSUFFICIENT DATA"

    latest = data.iloc[-1]

    if pd.isna(latest["RSI"]):
        return "INSUFFICIENT DATA"

    if latest["EMA20"] > latest["EMA50"] and latest["RSI"] > 50:
        return "BULLISH"

    if latest["EMA20"] < latest["EMA50"] and latest["RSI"] < 50:
        return "BEARISH"

    return "NEUTRAL"

@st.cache_data(ttl=300)
def get_market_data(ticker, interval, period):
    data = yf.Ticker(ticker).history(
        period=period,
        interval=interval
    )
    return analyse_market(data)

if st.button("🔄 REFRESH MARKETS"):
    st.cache_data.clear()

st.divider()
st.header("Market Overview")

for market, ticker in markets.items():
    st.subheader(market)

    try:
        data_15m = get_market_data(ticker, "15m", "5d")
        data_1h = get_market_data(ticker, "1h", "1mo")

        if data_15m.empty or data_1h.empty:
            st.warning("Market data currently unavailable.")
            continue

        latest = data_15m.iloc[-1]

        signal_15m = get_signal(data_15m)
        signal_1h = get_signal(data_1h)

        if signal_15m == signal_1h:
            bias = signal_15m
        else:
            bias = "NEUTRAL"

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Latest Price",
            f"{latest['Close']:.5f}"
        )

        col2.metric(
            "15m RSI",
            f"{latest['RSI']:.2f}"
            if pd.notna(latest["RSI"]) else "N/A"
        )

        col3.metric(
            "Market Bias",
            bias
        )

        st.write(
            f"15-minute trend: **{signal_15m}**"
        )

        st.write(
            f"1-hour trend: **{signal_1h}**"
        )
        st.caption(
    f"Chart points: {data_15m['Close'].notna().sum()} | "
    f"Unique prices: {data_15m['Close'].nunique()}"
        )
        st.line_chart(
            data_15m["Close"],
            height=180
        )

    except Exception as error:
        st.warning(f"Could not load {market}: {error}")

    st.divider()

st.info(
    "MarketPulse signals are educational indicators, "
    "not financial advice or guaranteed predictions."
)


import urllib.parse
import urllib.request

def send_telegram_message(message):
    token = st.secrets["BOT_TOKEN"]
    chat_id = st.secrets["CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message
    }).encode()

    request = urllib.request.Request(url, data=data)

    with urllib.request.urlopen(request, timeout=15) as response:
        return response.status == 200

st.divider()
st.header("📲 Telegram Notifications")

if st.button("Send Test Telegram Alert"):
    try:
        success = send_telegram_message(
            "🚀 MARKETPULSE\n\nTelegram connection successful!\nEducational paper-trading mode."
        )

        if success:
            st.success("Test alert sent successfully!")

    except Exception as error:
        st.error(
            f"Telegram error: {type(error).__name__}: {error}"
        )

st.divider()
st.header("📊 MarketPulse Trade Dashboard")

st.info("Educational signals only. Paper-trading mode.")

if "trade_history" not in st.session_state:
    st.session_state.trade_history = []

st.subheader("📈 Signal Confirmation")

ema20 = st.number_input("EMA 20", value=0.0, format="%.5f")
ema50 = st.number_input("EMA 50", value=0.0, format="%.5f")
rsi = st.number_input("RSI", min_value=0.0, max_value=100.0, value=50.0)

if ema20 > ema50 and rsi > 50:
    signal = "BULLISH"
elif ema20 < ema50 and rsi < 50:
    signal = "BEARISH"
else:
    signal = "NEUTRAL"

st.subheader("Current Market Signal")

if signal == "BULLISH":
    st.success("🟢 BULLISH")
elif signal == "BEARISH":
    st.error("🔴 BEARISH")
else:
    st.warning("🟡 NEUTRAL")

st.caption("Signals require EMA and RSI confirmation.")

st.divider()
st.subheader("📝 Paper Trade Journal")

market = st.text_input("Market", placeholder="e.g. EUR/USD")
entry = st.number_input("Entry Price", min_value=0.0, format="%.5f")
stop_loss = st.number_input("Stop Loss", min_value=0.0, format="%.5f")
take_profit = st.number_input("Take Profit", min_value=0.0, format="%.5f")

if st.button("Save Paper Trade"):
    if market and entry > 0 and stop_loss > 0 and take_profit > 0:
        st.session_state.trade_history.append({
            "Market": market,
            "Signal": signal,
            "Entry": entry,
            "Stop Loss": stop_loss,
            "Take Profit": take_profit
        })
        
