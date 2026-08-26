import requests

def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,solana",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def display_market_report(data):
    if not data:
        print("Could not display market report due to an error.")
        return

    print("\n" + "=" * 45)
    print(f"{'CRYPTO':<12} | {'PRICE (USD)':<12} | {'24H CHANGE':<10}")
    print("=" * 45)

    for coin, info in data.items():
        price = info.get("usd", 0.0)
        change_24h = info.get("usd_24h_change", 0.0)
        change_str = f"{change_24h:+.2f}%"
        print(f"{coin.upper():<12} | ${price:<11,.2f} | {change_str:<10}")

    print("=" * 45 + "\n")

if __name__ == "__main__":
    market_data = fetch_crypto_prices()
    display_market_report(market_data)