import asyncio
import os
import threading

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from dotenv import load_dotenv
from flask import Flask

from db import drop_table, init_db
from handlers.admin_handler import admin_router
from handlers.user_handler import router

load_dotenv()

# --------------------  ВЕБ - СЕРВЕР -------------------

app = Flask(__name__)

@app.route('/ping')
def home():
    return "pong"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
print("Веб-сервер запущен на порту", os.environ.get('PORT', 9000))

# -------------------- ТЕЛЕГРАМ БОТ -------------------


BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def set_main_menu():
    commands = [
        BotCommand(command='start', description='Начать'),
        BotCommand(command='sms', description='Отправить смс'),
        BotCommand(command='show', description='Показать все полученные сообщения'),
        BotCommand(command='help', description='Информация о боте')
    ]
    await bot.set_my_commands(commands)

# --------------------  MAIN -------------------

async def main():
    #await drop_table()
    await init_db()
    dp.startup.register(set_main_menu)  
    dp.include_routers(router, admin_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Выход...')

