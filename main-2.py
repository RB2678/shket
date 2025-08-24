import asyncio

import telebot
import requests
import os
import gdown
from flask import Flask, request
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random

TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")
bot = telebot.TeleBot(TOKEN, parse_mode=None)
messages = ["Тимур лох", "Тимур лох объелся блох", "Тимур блох объелся лох", "Тимур жопа", "Тимур пердун", "Тимур лошара", "Тимур шайтан", "Тимур ЛОХнесское чудовище",]
app = Flask(__name__)

async def send_message():
    message = random.choice(messages)
    await bot.send_message(chat_id=USER_ID, text=message)
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
        bot.send_message(message.chat.id, "Тимур лох, и я буду об этом напоминать тебе каждый месяц")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


if __name__ == "__main__":
    server_url = os.getenv("RENDER_EXTERNAL_URL")
    scheduler10 = AsyncIOScheduler()
    scheduler20 = AsyncIOScheduler()
    if server_url and TOKEN:
        webhook_url = f"{server_url}/{TOKEN}"
        set_webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}"
        try:
            r = requests.get(set_webhook_url)
            print("Webhook установлен:", r.text)
        except Exception as e:
            print("Ошибка при установке webhook:", e)

        port = int(os.environ.get("PORT", 10000))
        print(f"Starting server on port {port}")
        app.run(host='0.0.0.0', port=port)

        scheduler10.add_job(
            send_message(),
            'cron',
            day=10,
            hour=12,
            minute=30
        )

        scheduler20.add_job(
            send_message(),
            'cron',
            day=24,
            hour=17,
            minute=10
        )

        scheduler10.start()
        scheduler20.start()

        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            pass
    else:
        print("Запуск бота в режиме pooling")
        bot.remove_webhook()
        bot.polling(none_stop=True)
