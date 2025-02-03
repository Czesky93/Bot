from flask import Flask, render_template, request, jsonify
import os
import json
import time
import requests
from config_manager import load_config, save_config

app = Flask(__name__)

@app.route("/")
def home():
    config = load_config()
    return render_template("dashboard.html", config=config)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        new_config = request.json
        save_config(new_config)
        return jsonify({"status": "success", "message": "✅ Ustawienia zapisane!"})
    return jsonify(load_config())

@app.route("/start_bot", methods=["POST"])
def start_bot():
    os.system("python3 master_ai_trader.py &")
    return jsonify({"status": "success", "message": "🚀 Bot uruchomiony!"})

@app.route("/stop_bot", methods=["POST"])
def stop_bot():
    os.system("pkill -f master_ai_trader.py")
    return jsonify({"status": "success", "message": "🛑 Bot zatrzymany!"})

@app.route("/bot_status", methods=["GET"])
def bot_status():
    """Sprawdza czy bot działa"""
    output = os.popen("pgrep -f master_ai_trader.py").read()
    status = "✅ Bot działa" if output else "❌ Bot nie jest uruchomiony"
    return jsonify({"status": status})

@app.route("/market_analysis", methods=["GET"])
def market_analysis():
    """Pobiera aktualne ceny z Binance"""
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price")
        market_data = response.json()
        return jsonify(market_data)
    except Exception as e:
        return jsonify({"error": f"Błąd pobierania danych z Binance: {e}"})

@app.route("/get_logs", methods=["GET"])
def get_logs():
    """Pobiera ostatnie logi bota"""
    try:
        with open("bot.log", "r") as file:
            logs = file.readlines()[-10:]  # Pobranie ostatnich 10 linii logów
        return jsonify({"logs": logs})
    except FileNotFoundError:
        return jsonify({"logs": ["Brak logów!"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
