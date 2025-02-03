from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)  # ✅ Definicja aplikacji Flask przed użyciem dekoratorów!

CONFIG_FILE = "config.json"

# 📌 Funkcja do ładowania konfiguracji
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {}

# 📌 Strona główna – Dashboard
@app.route("/")
def home():
    config = load_config()
    return render_template("dashboard.html", config=config)

# 📌 Strona konfiguracji bota
@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        new_config = request.json
        with open(CONFIG_FILE, "w") as file:
            json.dump(new_config, file, indent=4)
        return jsonify({"status": "success", "message": "Ustawienia zapisane!"})

    config = load_config()
    return render_template("settings.html", config=config)

# 📌 API do zarządzania Binance
@app.route("/update_binance", methods=["POST"])
def update_binance():
    data = request.json
    binance_settings = {
        "api_key": data.get("binance_api_key"),
        "secret_key": data.get("binance_secret_key"),
        "mode": data.get("binance_mode"),
        "leverage": int(data.get("leverage", 10))
    }
    with open("binance_config.json", "w") as file:
        json.dump(binance_settings, file, indent=4)
    return jsonify({"status": "success", "message": "Ustawienia Binance zapisane!"})

# 📌 API do startowania i zatrzymywania bota
@app.route("/start_bot", methods=["POST"])
def start_bot():
    os.system("python3 master_ai_trader.py &")
    return jsonify({"status": "success", "message": "Bot uruchomiony!"})

@app.route("/stop_bot", methods=["POST"])
def stop_bot():
    os.system("pkill -f master_ai_trader.py")
    return jsonify({"status": "success", "message": "Bot zatrzymany!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
