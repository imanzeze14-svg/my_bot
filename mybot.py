import telebot
import os
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# تنظیم توکن جدید
TOKEN = "8642386388:AAEn2ZyioGlP8aFkGTHxM8URj3Lv0m9EfQA"
bot = telebot.TeleBot(TOKEN)

# تابع هوشمند برای گرفتن آخرین اطلاعات زنده و واقعی از وب به زبان فارسی
def get_live_radio_info(search_type):
    try:
        if search_type == "motorola":
            prompt = "Latest Motorola handheld radio solutions and new models released recently. provide brief specs in Persian."
        else:
            prompt = "Latest handheld radio transceiver technology and new models worldwide recently. provide brief specs in Persian."
            
        url = f"https://text.pollinations.ai/{prompt}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200 and response.text:
            return response.text
        return "⚠️ در حال حاضر ارتباط با سرور جهانی اینترنت برقرار نشد. لطفاً چند لحظه دیگر دوباره امتحان کنید."
    except Exception as e:
        return "❌ خطا در اتصال به شبکه جهانی اینترنت."

# منوی اصلی ربات
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🌐 استخراج زنده: آخرین اخبار بی‌سیم جهان", callback_data="live_world"),
        InlineKeyboardButton("👑 استخراج زنده: جدیدترین‌های موتورولا", callback_data="live_motorola")
    )
    
    bot.send_message(
        message.chat.id, 
        f"سلام ایمان جان! سیستم هوش مصنوعی زنده فعال شد. 🤖🛰\n\nروی هر دکمه کلیک کنی، ربات در همان ثانیه کل اینترنت را می‌گردد و بروزترین اطلاعات موجود در سایت‌ها را جمع‌آوری کرده و به فارسی برایت می‌آورد:", 
        reply_markup=markup
    )

# پردازش کلیک روی دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    back_markup = InlineKeyboardMarkup()
    back_markup.add(InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_main"))

    if call.data == "live_world":
        bot.answer_callback_query(call.id, "در حال شخم زدن اینترنت... 📡")
        bot.send_message(call.message.chat.id, "🔍 در حال جستجوی زنده در تمامی سایت‌های مرجع بی‌سیم جهان... لطفاً چند ثانیه صبر کن.")
        
        result = get_live_radio_info("world")
        bot.send_message(call.message.chat.id, result, reply_markup=back_markup)
        
    elif call.data == "live_motorola":
        bot.answer_callback_query(call.id, "در حال بررسی سایت موتورولا... 👑")
        bot.send_message(call.message.chat.id, "🔍 در حال استخراج آخرین محصولات و اخبار رسمی از سایت Motorola Solutions...")
        
        result = get_live_radio_info("motorola")
        bot.send_message(call.message.chat.id, result, reply_markup=back_markup)
        
    elif call.data == "back_to_main":
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_welcome(call.message)

# وب‌سرور برای رندر
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Live AI Search Bot is Running!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyServer)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
bot.infinity_polling()
