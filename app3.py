import streamlit as st
import requests

st.set_page_config(page_title="Crypto Tracker", page_icon="📈")

st.title("📈 Real-Time Crypto Tracker")
st.write("Fetch live prices and market data using Python & Streamlit.")

# Sidebar controls
coins_to_fetch = st.sidebar.multiselect(
    "Select Cryptocurrencies:",
    ["bitcoin", "ethereum", "solana", "cardano", "ripple"],
    default=["bitcoin", "ethereum", "solana"]
)

if st.button("Refresh Market Data"):
    if not coins_to_fetch:
        st.warning("Please select at least one cryptocurrency.")
    else:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": ",".join(coins_to_fetch),
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        
        with st.spinner("Fetching latest prices..."):
            try:
                response = requests.get(url, params=params, timeout=10)
                data = response.json()
                
                # Render in interactive UI columns
                cols = st.columns(len(coins_to_fetch))
                for idx, coin in enumerate(coins_to_fetch):
                    if coin in data:
                        price = data[coin].get("usd", 0.0)
                        change = data[coin].get("usd_24h_change", 0.0)
                        cols[idx].metric(
                            label=coin.upper(),
                            value=f"${price:,.2f}",
                            delta=f"{change:+.2f}%"
                        )
            except Exception as e:
                st.error(f"Failed to fetch market data: {e}")