import telebot
import os
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# ۱. تنظیمات توکن ربات
TOKEN = "8642386388:AAEhGZn73Coiv6bNysv96Jxya4SSb73fw2E"
bot = telebot.TeleBot(TOKEN)

# تابع کمکی برای جستجوی زنده در وب
def search_web(query):
    try:
        # استفاده از یک API رایگان و بدون تحریم برای جستجوی زنده در وب
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # اگر اطلاعات مستقیمی پیدا شد
        if data.get("AbstractText"):
            return data["AbstractText"]
        # اگر نتایج مرتبط دیگری وجود داشت
        elif data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
            return data["RelatedTopics"][0].get("Text", "اطلاعاتی پیدا نشد.")
        else:
            return "متأسفانه نتوانستم اطلاعات زنده جدیدی دریافت کنم. لطفا دوباره تلاش کنید."
    except Exception as e:
        return "خطا در اتصال به شبکه جهانی اینترنت برای دریافت اطلاعات."

# ۲. منوی اصلی ربات
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("📡 آخرین اخبار بی‌سیم در جهان", callback_data="news_world"),
        InlineKeyboardButton("🔥 جدیدترین تکنولوژی موتورولا (Motorola)", callback_data="news_motorola"),
        InlineKeyboardButton("✍️ جستجوی دلخواه (راهنما)", callback_data="search_help")
    )
    
    bot.send_message(
        message.chat.id, 
        f"سلام ایمان جان! به مرکز اطلاعات هوشمند بی‌سیم خوش آمدی. 🌐\n\nیک گزینه را انتخاب کن تا ربات همین الان برود اینترنت را بگردد و اطلاعات بروز را برایت بیاورد:", 
        reply_markup=markup
    )

# ۳. پردازش کلیک روی دکمه‌ها و جستجوی زنده
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "در حال جستجو در وب... ⏳")
    
    if call.data == "news_world":
        bot.send_message(call.message.chat.id, "🔍 در حال بررسی آخرین اخبار بی‌سیم‌های دستی در جهان...")
        result = search_web("latest handheld radio transceiver technology news 2026")
        bot.send_message(call.message.chat.id, f"🌐 **آخرین اطلاعات یافت شده در وب:**\n\n{result}")
        
    elif call.data == "news_motorola":
        bot.send_message(call.message.chat.id, "🔍 در حال سرچ جدیدترین محصولات و اخبار موتورولا Solutions...")
        result = search_web("latest Motorola solutions handheld radio APX MOTOTRBO 2026")
        bot.send_message(call.message.chat.id, f"👑 **جدیدترین‌ها از موتورولا:**\n\n{result}")
        
    elif call.data == "search_help":
        bot.send_message(
            call.message.chat.id, 
            "💡 **راهنمای جستجوی هوشمند:**\nکافیست اسم هر بی‌سیمی که می‌خواهی را بنویسی و بفرستی، ربات خودش می‌رود مشخصاتش را پیدا می‌کند!"
        )

# ۴. جستجوی خودکار وقتی کاربر اسم یک بی‌سیم را پیامک می‌کند
@bot.message_handler(func=lambda message: True)
def auto_search(message):
    user_query = message.text
    bot.send_message(message.chat.id, f"🔍 دارم توی کل اینترنت دنبال '{user_query}' می‌گردم، یه لحظه صبر کن...")
    result = search_web(user_query)
    bot.send_message(message.chat.id, f"📄 **نتایج پیدا شده برای شما:**\n\n{result}")

# ۵. وب‌سرور فیک برای رندر
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"AI Bot with Web Search is Live!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyServer)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
bot.infinity_polling()


