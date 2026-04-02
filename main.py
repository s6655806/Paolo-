import os
from flask import Flask
import telebot
from threading import Thread

app = Flask(__name__)

# الصفحة الرئيسية عشان الرابط يشتغل في MoboEasy
@app.route('/')
def home():
    return "<h1>Carlos Bot is Online!</h1>"

# التوكن الخاص بك
TOKEN = "8754467241:AAHTlQY26Nn0keE4B9H-SVLRCD1G4NwyHJI"
bot = telebot.TeleBot(TOKEN)

# أمر الترحيب المعدل بناءً على طلبك
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أنا نسخة كارلوس مولد الفيديو والصور.")

# تشغيل سيرفر ويب صغير
def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# تشغيل البوت والسيرفر مع بعض
if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
