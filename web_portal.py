from flask import Flask, render_template, request, jsonify
import os
import json
import requests
import subprocess

app = Flask(__name__)

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {}

def save_config(new_config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(new_config, file, indent=4)

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
    config = load_config()
    return render_template("settings.html", config=config)

@app.route("/start_bot", methods=["POST"])
def start_bot():
    try:
        subprocess.Popen(["python3", "master_ai_trader.py"])
        return jsonify({"status": "success", "message": "🚀 Bot uruchomiony!"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"❌ Błąd uruchamiania bota: {str(e)}"})

@app.route("/stop_bot", methods=["POST"])
def stop_bot():
    try:
        os.system("pkill -f master_ai_trader.py")
        return jsonify({"status": "success", "message": "🛑 Bot zatrzymany!"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"❌ Błąd zatrzymywania bota: {str(e)}"})

@app.route("/market_analysis", methods=["GET"])
def market_analysis():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price")
        market_data = response.json()
        return jsonify({"status": "success", "market_data": market_data})
    except Exception as e:
        return jsonify({"status": "error", "message": f"❌ Błąd pobierania danych: {str(e)}"})

@app.route("/get_logs", methods=["GET"])
def get_logs():
    logs_file = "bot_logs.txt"
    if os.path.exists(logs_file):
        with open(logs_file, "r") as file:
            logs = file.readlines()
        return jsonify({"status": "success", "logs": logs})
    return jsonify({"status": "error", "logs": ["⚠️ Brak logów!"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
