import json
import os
from binance.client import Client

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError("🚨 Plik config.json nie istnieje!")

    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

config = load_config()
API_KEY = config.get("binance_api_key", "")
API_SECRET = config.get("binance_api_secret", "")

if not API_KEY or not API_SECRET:
    raise ValueError("❌ Brak kluczy API Binance w config.json!")

client = Client(API_KEY, API_SECRET)

def place_order(symbol, amount, side="BUY"):
    try:
        order = client.order_market(symbol=symbol, quantity=amount, side=side)
        return order
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    result = place_order(config["trading_pair"], 0.001)
    print(result)
