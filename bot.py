import os
from flask import Flask
import telebot
from threading import Thread
import requests
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/')
def home():
    return "<h1>Carlos Bot is Online!</h1>"

# التوكن الشغال والنهائي
TOKEN = "8754467241:AAFAJvEOrzb3fRtcqjX9r-hn6Qz_erqZbhA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في نسخة كارلوس. أرسل وصفك بالعربي (مثلاً: صورة أسد، أو فيديو فضاء) وسأقوم بالتوليد فوراً.")

@bot.message_handler(func=lambda message: True)
def generate_media(message):
    user_msg = message.text
    if len(user_msg) < 3:
        return

    bot.reply_to(message, "جاري الترجمة والمعالجة.. انتظر قليلاً ⏳")
    
    try:
        # ترجمة النص للإنجليزية ليفهمه محرك التوليد
        translation = translator.translate(user_msg, dest='en')
        translated_text = translation.text
        clean_prompt = requests.utils.quote(translated_text)
        
        msg_lower = user_msg.lower()
        
        # إذا طلب المستخدم فيديو
        if any(word in msg_lower for word in ["فيديو", "video", "متحرك"]):
            video_url = f"https://pollinations.ai/p/{clean_prompt}?model=video"
            bot.send_animation(message.chat.id, video_url, caption=f"🎬 تم التوليد لـ: {translated_text}")

        # إذا طلب المستخدم صورة
        elif any(word in msg_lower for word in ["صورة", "photo", "image", "صوره"]):
            image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024"
            bot.send_photo(message.chat.id, image_url, caption=f"🎨 تم التوليد لـ: {translated_text}")
            
        else:
            bot.reply_to(message, "يا غالي، حدد في رسالتك كلمة (صورة) أو (فيديو) عشان أعرف طلبك بالظبط.")
            
    except Exception as e:
        bot.reply_to(message, "حدث ضغط بسيط، أعد إرسال طلبك مرة أخرى.")

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
