import threading
import asyncio
from flask import Flask
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers.user_handler import router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route('/ping')
def home():
    return "pong"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
print("Веб-сервер запущен на порту", os.environ.get('PORT', 8080))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


