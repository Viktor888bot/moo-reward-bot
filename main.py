import json
import time
import telebot
from datetime import datetime, timedelta

API_TOKEN = '7623462991:AAHdAvrsn3Hzo34DR1J-4E3K4Xdwy32hhTs'  # 

bot = telebot.TeleBot(API_TOKEN)

DATA_FILE = 'users.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    data = load_data()
    if user_id not in data:
        data[user_id] = {"balance": 0, "last_bonus": "2000-01-01"}
        save_data(data)
    bot.send_message(message.chat.id, "Привет! Это Moo бот! Получай бонусы каждый день с командой /bonus.")

@bot.message_handler(commands=['balance'])
def balance(message):
    user_id = str(message.from_user.id)
    data = load_data()
    bal = data.get(user_id, {}).get("balance", 0)
    bot.send_message(message.chat.id, f"Ваш баланс: {bal} баллов.")

@bot.message_handler(commands=['bonus'])
def bonus(message):
    user_id = str(message.from_user.id)
    data = load_data()
    user = data.get(user_id)
    if not user:
        user = {"balance": 0, "last_bonus": "2000-01-01"}
    last = datetime.strptime(user["last_bonus"], "%Y-%m-%d")
    now = datetime.now()
    if now - last >= timedelta(days=1):
        user["balance"] += 10
        user["last_bonus"] = now.strftime("%Y-%m-%d")
        data[user_id] = user
        save_data(data)
        bot.send_message(message.chat.id, "Вы получили 10 баллов за сегодня!")
    else:
        bot.send_message(message.chat.id, "Вы уже получили бонус сегодня. Приходите завтра!")

print("Бот запущен...")
bot.infinity_polling()
