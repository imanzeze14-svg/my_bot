import telebot
import os
import requests
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# تنظیم توکن جدید شما
TOKEN = "8642386388:AAEn2ZyioGlP8aFkGTHxM8URj3Lv0m9EfQA"
bot = telebot.TeleBot(TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_official_news(brand):
    try:
        if brand == "motorola":
            url = "https://www.motorolasolutions.com/en_us/newsroom.html"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 200:
                titles = re.findall(re.compile(r'<h3[^>]*>(.*?)</h3>', re.DOTALL), response.text)[:3]
                if titles:
                    result = "👑 **آخرین عناوین رسمی از سایت Motorola Solutions:**\n\n"
                    for i, title in enumerate(titles, 1):
                        clean_title = re.sub('<[^<]+?>', '', title).strip()
                        result += f"{i}️⃣ {clean_title}\n\n"
                    return result
            return "⚠️ سایت موتورولا در حال حاضر اجازه استخراج دیتای زنده را نداد."

        elif brand == "hytera":
            url = "https://www.hytera.com/en/media-center/news.html"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 200:
                titles = re.findall(re.compile(r'<h4[^>]*>(.*?)</h4>', re.DOTALL), response.text)[:3]
                if titles:
                    result = "⚡ **آخرین عناوین رسمی از سایت Hytera:**\n\n"
                    for i, title in enumerate(titles, 1):
                        clean_title = re.sub('<[^<]+?>', '', title).strip()
                        result += f"{i}️⃣ {clean_title}\n\n"
                    return result
            return "⚠️ سایت هایترا در حال حاضر پاسخ نداد."

    except Exception as e:
        return "❌ خطا در اتصال مستقیم به سرور سایت مرجع."

# منوی اصلی ربات
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("👑 استخراج مستقیم از سایت Motorola", callback_data="get_motorola"),
        InlineKeyboardButton("⚡ استخراج مستقیم از سایت Hytera", callback_data="get_hytera")
    )
    
    bot.send_message(
        message.chat.id, 
        f"سلام ایمان جان! ربات بدون نیاز به ابزار اضافی فعال شد. 🛰\n\nروی هر دکمه کلیک کنی، ربات مستقیماً وارد سایت مرجع شده و جدیدترین عناوین را برایت می‌آورد:", 
        reply_markup=markup
    )

# پردازش کلیک دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    back_markup = InlineKeyboardMarkup()
    back_markup.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main"))

    if call.data == "get_motorola":
        bot.answer_callback_query(call.id, "اتصال به موتورولا... 📡")
        bot.send_message(call.message.chat.id, "🔍 در حال ورود به سایت رسمی Motorola Solutions...")
        res = get_official_news("motorola")
        bot.send_message(call.message.chat.id, res, reply_markup=back_markup)
        
    elif call.data == "get_hytera":
        bot.answer_callback_query(call.id, "اتصال به هایترا... ⚡")
        bot.send_message(call.message.chat.id, "🔍 در حال ورود به سایت رسمی Hytera...")
        res = get_official_news("hytera")
        bot.send_message(call.message.chat.id, res, reply_markup=back_markup)
        
    elif call.data == "back_to_main":
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_welcome(call.message)

# وب‌سرور رندر
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Official Fast Scraper Bot is Running!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyServer)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
bot.infinity_polling()

