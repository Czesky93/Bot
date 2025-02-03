@app.route("/update_binance", methods=["POST"])
def update_binance():
    data = request.json
    binance_settings = {
        "api_key": data["binance_api_key"],
        "secret_key": data["binance_secret_key"],
        "mode": data["binance_mode"],
        "leverage": int(data["leverage"])
    }
    with open("binance_config.json", "w") as file:
        json.dump(binance_settings, file, indent=4)
    return jsonify({"status": "success", "message": "Ustawienia Binance zapisane!"})

@app.route("/update_telegram", methods=["POST"])
def update_telegram():
    data = request.json
    telegram_settings = {
        "token": data["telegram_token"],
        "mode": data["telegram_mode"]
    }
    with open("telegram_config.json", "w") as file:
        json.dump(telegram_settings, file, indent=4)
    return jsonify({"status": "success", "message": "Ustawienia Telegram zapisane!"})

@app.route("/update_ai", methods=["POST"])
def update_ai():
    data = request.json
    ai_settings = {
        "mode": data["ai_mode"],
        "risk_level": int(data["risk_level"])
    }
    with open("ai_config.json", "w") as file:
        json.dump(ai_settings, file, indent=4)
    return jsonify({"status": "success", "message": "Ustawienia AI zapisane!"})
