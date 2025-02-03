import telepot
import json
import os
from binance_trader import place_order

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError("🚨 Plik config.json nie istnieje!")

    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

config = load_config()
TOKEN = config.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = config.get("TELEGRAM_CHAT_ID", "")

if not TOKEN or not CHAT_ID:
    raise ValueError("❌ Brak konfiguracji Telegrama w config.json!")

bot = telepot.Bot(TOKEN)

def send_telegram_message(message):
    try:
        bot.sendMessage(CHAT_ID, message)
    except Exception as e:
        print(f"❌ Błąd wysyłania wiadomości: {e}")

def handle_message(msg):
    text = msg["text"].strip().lower()
    
    if text == "/start":
        send_telegram_message("🚀 RLdC Trading Bot aktywowany!")
    elif text == "/status":
        send_telegram_message("✅ Bot działa i jest połączony z Telegramem.")
    elif text == "/trade":
        send_telegram_message("📈 Realizacja zlecenia...")
        result = place_order(config["trading_pair"], 0.001)
        send_telegram_message(f"📊 Wynik: {result}")
    else:
        send_telegram_message("❓ Nieznana komenda! Dostępne komendy:\n/start\n/status\n/trade")

bot.message_loop(handle_message)
send_telegram_message("✅ Telegram AI Bot uruchomiony i gotowy do działania!")

import time
while True:
    time.sleep(5)
