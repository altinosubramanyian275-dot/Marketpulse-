import streamlit as st

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

st.divider()

st.header("Market Overview")

markets = ["EUR/USD", "GBP/USD", "USD/JPY", "BTC/USD"]

columns = st.columns(2)

for i, market in enumerate(markets):
    with columns[i % 2]:
        st.metric(
            label=market,
            value="Awaiting data",
            delta="Not connected"
        )

st.info("Market data connection coming next.")

st.success("MARKETPULSE WEBSITE INITIALISED")
