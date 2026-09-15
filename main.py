import telebot, json, os, threading
from datetime import datetime
from flask import Flask

TOKEN = '8823404473:AAGhcEuCYotTtpNTsaMUs8wFOVfYNdcLrGg'
bot = telebot.TeleBot(TOKEN)
FILE = 'users_data.json'

def load():
    if os.path.exists(FILE):
        try:
            with open(FILE,'r',encoding='utf-8') as f: return json.load(f)
        except: return {}
    return {}

def save(d):
    with open(FILE,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=4)

users = load()
kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
kb.add('БАРБЕРШОП','АВТОМОЙКА','КОФЕЙНЯ')

@bot.message_handler(commands=['start'])
def s(m): bot.send_message(m.chat.id,"Салам! Выбирай и забирай купон 1 раз в месяц 🔥",reply_markup=kb)

@bot.message_handler(func=lambda m: m.text in ['БАРБЕРШОП','АВТОМОЙКА','КОФЕЙНЯ'])
def c(m):
    uid=str(m.from_user.id); cat=m.text; today=datetime.now().strftime("%Y-%m-%d")
    if uid in users and cat in users[uid]:
        if datetime.strptime(users[uid][cat],"%Y-%m-%d").month==datetime.now().month:
            bot.send_message(m.chat.id,f"Брат, {cat} уже брал в этом месяце 😅"); return
    if uid not in users: users[uid]={}
    users[uid][cat]=today; save(users)
    co={'БАРБЕРШОП':'BARBER10 - 10% на стрижку','АВТОМОЙКА':'WASH20 - 5 моек = 1 бесплатно','КОФЕЙНЯ':'COFFEE500 - Кофе+десерт 1500тг'}
    bot.send_message(m.chat.id,f"Держи купон на {cat}! 🔥\n\n{co[cat]}")

# Чтобы Render не ругался
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

def run_bot(): bot.polling(none_stop=True)
threading.Thread(target=run_bot,daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))