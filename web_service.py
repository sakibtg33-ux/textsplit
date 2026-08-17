import os
import threading

from flask import Flask

from bot import main as run_telegram_bot

app = Flask(__name__)


@app.get("/")
def health_check():
    return "TXT split Telegram bot is running", 200


@app.get("/health")
def health():
    return {"status": "ok"}, 200


def run_web_server() -> None:
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, use_reloader=False)


if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    run_telegram_bot()
