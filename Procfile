web: gunicorn web_portal:app --log-file -
worker: python3 master_ai_trader.py
worker: python3 ai_optimizer.py
worker: python3 pump_dump_detector.py
worker: python3 news_watcher.py
worker: python3 telegram_ai_bot.py
