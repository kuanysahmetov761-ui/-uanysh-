import os
import telebot
from telebot import types
import sqlite3
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8696556885

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('leads.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS leads
                  (user_id INTEGER, shop TEXT, month TEXT,
                  UNIQUE(user_id, shop, month))''')
conn.commit()

COUPONS = {
    "БАРБЕРШОП": "BARBER10 - 10% на стрижку",
    "АВТОМОЙКА": "WASH20 - 5 моек = 1 бесплатно",
    "КОФЕЙНЯ": "COFFEE500 - Кофе + десерт за 1500тг"
}

def get_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("БАРБЕРШОП", "АВТОМОЙКА")
    markup.add("КОФЕЙНЯ")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Забирай купон 1 раз в месяц 👇", reply_markup=get_menu())

@bot.message_handler(func=lambda m: m.text in COUPONS)
def give_coupon(message):
    shop = message.text
    month = datetime.now().strftime("%Y-%m")
    user_id = message.from_user.id
    cursor.execute("SELECT 1 FROM leads WHERE user_id=? AND shop=? AND month=?", (user_id, shop, month))
    if cursor.fetchone():
        bot.send_message(message.chat.id, f"Брат, купон на {shop} ты уже брал в этом месяце 😅")
        return
    try:
        cursor.execute("INSERT INTO leads (user_id, shop, month) VALUES (?,?,?)", (user_id, shop, month))
        conn.commit()
        bot.send_message(message.chat.id, f"Держи купон на {shop}! 🔥\n\n{ COUPONS[shop] }")
    except:
        bot.send_message(message.chat.id, f"Брат, купон на {shop} ты уже брал в этом месяце 😅")

print("Скидки KZ Агент запущен!")
bot.polling(none_stop=True)
