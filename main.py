import telebot
import requests
import json

bot = telebot.TeleBot("7878536544:AAHncWeSsm4qr6anofT1FSvRqqi5_KNKqhg")
API = "534a3d849a6260ed8739eec0cd69418e"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Рад тебя видеть! Напиши название города")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    coordinates = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API}")
    data_coordinates = json.loads(coordinates.text)

    if data_coordinates:
        lat = data_coordinates[0]["lat"]
        lon = data_coordinates[0]["lon"]
        res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API}&units=metric")
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f"Сейчас погода: {temp}")

        image = "sunny.jpg" if temp > 5.0 else "sun_cloud.jpg"
        file = open("./" + image, "rb")
        bot.send_photo(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, "Город указан неверно!")


bot.polling(none_stop=True)
