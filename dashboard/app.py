import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Cryptoline Dashboard",
    layout="wide",
)


conn = st.connection("postgresql", type="sql")


def load_view(view_name: str) -> pd.DataFrame:
    """Load an approved PostgreSQL view into a pandas DataFrame."""
    allowed_views = {
        "latest_crypto_prices",
        "top_10_crypto_by_market_cap",
        "top_10_crypto_by_volume",
        "top_10_crypto_gainers_24h",
        "top_10_crypto_losers_24h",
    }

    if view_name not in allowed_views:
        raise ValueError(f"View not allowed: {view_name}")

    return conn.query(f"SELECT * FROM {view_name};", ttl=300)


st.title("Cryptoline Dashboard")

latest_prices = load_view("latest_crypto_prices")
top_market_cap = load_view("top_10_crypto_by_market_cap")
top_volume = load_view("top_10_crypto_by_volume")
top_gainers = load_view("top_10_crypto_gainers_24h")
top_losers = load_view("top_10_crypto_losers_24h")

total_coins = len(latest_prices)
total_market_cap = latest_prices["market_cap"].sum()
total_volume = latest_prices["total_volume"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Tracked Coins", total_coins)
col2.metric("Total Market Cap", f"${total_market_cap:,.0f}")
col3.metric("Total Volume", f"${total_volume:,.0f}")

st.divider()

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Top 10 By Market Cap")
    st.bar_chart(top_market_cap.set_index("symbol")["market_cap"])

with right_col:
    st.subheader("Top 10 By Trading Volume")
    st.bar_chart(top_volume.set_index("symbol")["total_volume"])

st.divider()

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Top 10 Gainers 24h")
    st.dataframe(
        top_gainers[
            [
                "symbol",
                "name",
                "current_price",
                "price_change_percentage_24h",
            ]
        ],
        use_container_width=True,
    )

with right_col:
    st.subheader("Top 10 Losers 24h")
    st.dataframe(
        top_losers[
            [
                "symbol",
                "name",
                "current_price",
                "price_change_percentage_24h",
            ]
        ],
        use_container_width=True,
    )

st.divider()

st.subheader("Latest Crypto Prices")
st.dataframe(
    latest_prices.sort_values("market_cap", ascending=False),
    use_container_width=True,
)