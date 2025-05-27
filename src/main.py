import os
import telebot
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Обработчики базовых команд
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-астролог. Используй /horoscope чтобы получить свой гороскоп!")

# Функция для получения данных гороскопа
def get_daily_horoscope(sign: str, day: str) -> dict:
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)
    return response.json()

# Обработчики гороскопа
@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "Какой у вас знак зодиака?\nВыберите один: *Aries*, *Taurus*, *Gemini*, *Cancer*, *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    sign = message.text
    text = "На какой день показать гороскоп?\nВыберите: *TODAY*, *TOMORROW*, *YESTERDAY*, или дату (YYYY-MM-DD)."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign.capitalize())

def fetch_horoscope(message, sign):
    day = message.text
    try:
        horoscope = get_daily_horoscope(sign, day)
        data = horoscope["data"]
        response = f"*{sign}* на *{data['date']}*\n\n{data['horoscope_data']}"
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Ошибка получения данных. Попробуйте снова.")

# Обработка всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Используйте команду /horoscope для получения гороскопа!")

# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()