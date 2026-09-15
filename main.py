import telebot
from telebot import types
import os
import threading
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("ОШИБКА: BOT_TOKEN не задан!")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)
@app.route('/')
def home():
    return "Бот Скидки KZ работает!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("💈 БАРБЕРШОП"), types.KeyboardButton("🚗 АВТОМОЙКА"))
    markup.add(types.KeyboardButton("☕ КОФЕЙНЯ"), types.KeyboardButton("📱 СВЯЗЬ"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я агент Скидки KZ 👋\nВыбери бизнес, сделаю пост за 30 сек:", reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text
    if "БАРБЕРШОП" in text:
        bot.send_message(message.chat.id, "💈 Для барбершопа:\n\n'Стрижка + борода всего 4000тг! Запишись сегодня - осталось 3 места. Пиши в личку!' \n\nХочешь такой пост с твоим адресом?")
    elif "АВТОМОЙКА" in text:
        bot.send_message(message.chat.id, "🚗 Для автомойки:\n\n'Комплекс всего за 2500тг! До конца недели. Блеск как с салона ✨'")
    elif "КОФЕЙНЯ" in text:
        bot.send_message(message.chat.id, "☕ Для кофейни:\n\n'2 капучино по цене 1 до 12:00! Успей на завтрак ☕️'")
    else:
        bot.send_message(message.chat.id, "Напиши что за бизнес у тебя, я сделаю продающий пост!", reply_markup=main_menu())

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Скидки KZ Агент запущен!")
    bot.infinity_polling()
