import threading
import time
from flask import Flask
import telebot
import os
from dotenv import load_dotenv

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

bot = telebot.TeleBot(BOT_TOKEN)



@bot.message_handler(commands=['sms', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
        Привет! Хочешь представится как нибудь? (необязательно) 
    """)


    
@bot.message_handler()
def dialogue(message):
    name = "anonymous"
    #if dialogueIsStarted is True:
    #    bot.reply_to(message, """\
    #        "Напиши свое послание!!!" + name
    #    """)


print("Бот запущен")


while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)