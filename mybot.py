import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TOKEN = "8642386388:AAEhGZn73Coiv6bNysv96Jxya4SSb73fw2E"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("👑 کانال من", url="https://t.me/telegram"),
        InlineKeyboardButton("🚀 دکمه جادویی", callback_data="magic_click")
    )
    bot.send_message(
        message.chat.id, 
        f"سلام ایمان جان! به ربات پیشرفته خودت خوش آمدی. 🔥\nالان ربات کامل شده و آماده دستورات شماست!", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "magic_click":
        bot.answer_callback_query(call.id, "اینم از دکمه جادویی ربات شما! 😉")
        bot.send_message(call.message.chat.id, "🎉 ایول! دکمه‌ها دارن مثل ساعت کار می‌کنن حاجی!")

class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and advanced!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyServer)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
bot.infinity_polling()

