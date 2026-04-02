import os
from flask import Flask
import telebot
from threading import Thread
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Carlos Bot is Online!</h1>"

# التوكن الشغال 100%
TOKEN = "8754467241:AAFAJvEOrzb3fRtcqjX9r-hn6Qz_erqZbhA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً يا صلاح.. أنا نسخة كارلوس. أرسل وصفك بالإنجليزية حالياً (صورة أو فيديو) وسأقوم بالتوليد فوراً.")

@bot.message_handler(func=lambda message: True)
def generate_media(message):
    user_msg = message.text
    if len(user_msg) < 2: return

    bot.reply_to(message, "جاري المعالجة.. انتظر لحظة ⏳")
    
    try:
        clean_prompt = requests.utils.quote(user_msg)
        msg_lower = user_msg.lower()
        
        # كشف نوع الطلب
        if "video" in msg_lower or "gif" in msg_lower:
            url = f"https://pollinations.ai/p/{clean_prompt}?model=video"
            bot.send_animation(message.chat.id, url, caption="🎬 Done!")
        else:
            url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024"
            bot.send_photo(message.chat.id, url, caption="🎨 Done!")
            
    except Exception as e:
        bot.reply_to(message, "حدث خطأ، حاول مرة أخرى.")

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
