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
TOKEN = "8754467241:AAHTlQY26Nn0keE4B9H-SVLRCD1G"
