
import os, sqlite3, threading, time
from datetime import datetime
import telebot
from telebot import types
from flask import Flask

TOKEN = os.getenv("BOT_TOKEN")  or "8823404473:AAHtycrXUO7kVtSmnSgbt7RYizAAwh5lrO8"
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

ADMIN_NAME = "Ахметов Куаныш Нурланович"
ADMIN_PHONE = "87778937645"
ADMIN_WA = "https://wa.me/7778937645"

conn = sqlite3.connect('leads.db', check_same_thread=False)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS leads (user_id INT, shop TEXT, month TEXT, UNIQUE(user_id, shop, month))')
conn.commit()

COUPONS = {
    "💈 БАРБЕРШОП": ("BARBER-4000", "Стрижка+борода 4000тг! Осталось 3 места"),
    "🚗 АВТОМОЙКА": ("MOYKA-2500", "Комплекс 2500тг! Блеск как с салона"),
    "☕ КОФЕЙНЯ": ("COFFEE-15", "Кофе+десерт 1500тг")
}

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("💈 БАРБЕРШОП", "🚗 АВТОМОЙКА")
    kb.add("☕ КОФЕЙНЯ")
    return kb

@app.route('/')
def home(): return "Скидки KZ Агент - LIVE"

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f"Салам! Выбери купон 👇\n1 чел = 1 купон в месяц\n\nАдмин: {ADMIN_NAME}", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text in COUPONS)
def give(m):
    shop = m.text
    code, desc = COUPONS[shop]
    month = datetime.now().strftime("%Y-%m")
    uid = m.from_user.id

    cur.execute("SELECT 1 FROM leads WHERE user_id=? AND shop=? AND month=?", (uid, shop, month))
    if cur.fetchone():
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(f"📞 {ADMIN_NAME} {ADMIN_PHONE}", url=ADMIN_WA))
        bot.send_message(m.chat.id, f"⛔ Ты уже брал {shop} в этом месяце!\n1 чел = 1 купон.", reply_markup=kb)
        return

    cur.execute("INSERT INTO leads VALUES (?,?,?)", (uid, shop, month))
    conn.commit()

    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton(f"🎟️ Код: {code}", callback_data="ok"),
        types.InlineKeyboardButton(f"📞 {ADMIN_NAME}", url=ADMIN_WA)
    )
    bot.send_message(m.chat.id, f"🔥 {shop}\n\nКод: {code}\n{desc}\n\nПокажи на кассе!", reply_markup=kb)

def polling():
    while True:
        try: bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e: time.sleep(5)

threading.Thread(target=polling, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
