import os
import random
import logging
import requests
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
import telebot
from threading import Thread

TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")
server_url = os.getenv("RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

messages = [
    "Тимур лох",
    "Тимур лох объелся блох",
    "Тимур блох объелся лох",
    "Тимур жопа",
    "Тимур пердун",
    "Тимур лошара",
    "Тимур шайтан",
    "Тимур ЛОХнесское чудовище",
]

def send_message():
    try:
        message = random.choice(messages)
        bot.send_message(chat_id=USER_ID, text=message)
        logging.info(f"Отправлено сообщение: {message}")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")

@app.route('/')
def index():
    return "Bot is running"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.send_message(
            message.chat.id,
            "Тимур лох, и я буду об этом напоминать тебе 6 раз в месяц 😈"
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if server_url and TOKEN:
        webhook_url = f"{server_url}/{TOKEN}"
        set_webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}"
        try:
            r = requests.get(set_webhook_url)
            logging.info(f"Webhook установлен: {r.text}")
        except Exception as e:
            logging.error(f"Ошибка при установке webhook: {e}")
            
        Thread(target=run_flask, daemon=True).start()

        scheduler = BackgroundScheduler()
        scheduler.add_job(send_message, 'cron', day=5, hour=12, minute=30)
        scheduler.add_job(send_message, 'cron', day=10, hour=12, minute=30)
        scheduler.add_job(send_message, 'cron', day=15, hour=12, minute=30)
        scheduler.add_job(send_message, 'cron', day=20, hour=12, minute=30)
        scheduler.add_job(send_message, 'cron', day=25, hour=12, minute=30)
        scheduler.add_job(send_message, 'cron', day=30, hour=12, minute=30)
        scheduler.start()

        logging.info("Бот запущен. Ожидание событий...")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()
            logging.info("Бот остановлен.")

    else:
        logging.info("Запуск бота в режиме polling")
        bot.remove_webhook()
        bot.polling(none_stop=True)
