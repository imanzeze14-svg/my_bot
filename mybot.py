import telebot
import os
import requests
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request

# ۱. تنظیمات اصلی ربات
TOKEN = "8642386388:AAEn2ZyioGlP8aFkGTHxM8URj3Lv0m9EfQA"
bot = telebot.TeleBot(TOKEN, threaded=False)

# ساخت سرور وب با Flask برای حذف کامل ارور 409
app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# تابع جستجوی مستقیم در سایت‌های مرجع
def search_radio_website(brand):
    try:
        if brand == "motorola":
            url = "https://www.motorolasolutions.com/en_us/newsroom.html"
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                titles = re.findall(re.compile(r'<h3[^>]*>(.*?)</h3>', re.DOTALL), response.text)[:3]
                if titles:
                    result = "👑 **[IMAN-BOT] عناوین استخراج شده از Motorola Solutions:**\n\n"
                    for i, title in enumerate(titles, 1):
                        clean_title = re.sub('<[^<]+?>', '', title).strip()
                        result += f"{i}️⃣ {clean_title}\n\n"
                    return result
            return "⚠️ سایت موتورولا در حال حاضر اجازه دسترسی به دیتای زنده را نداد."

        elif brand == "hytera":
            url = "https://www.hytera.com/en/media-center/news.html"
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                titles = re.findall(re.compile(r'<h4[^>]*>(.*?)</h4>', re.DOTALL), response.text)[:3]
                if titles:
                    result = "⚡ **[IMAN-BOT] عناوین استخراج شده از Hytera:**\n\n"
                    for i, title in enumerate(titles, 1):
                        clean_title = re.sub('<[^<]+?>', '', title).strip()
                        result += f"{i}️⃣ {clean_title}\n\n"
                    return result
            return "⚠️ سایت هایترا در حال حاضر پاسخ نداد."

    except Exception:
        return "❌ خطا در برقراری ارتباط زنده با سایت مرجع."

# ۲. دستور شروع ربات
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("👑 استخراج زنده از موتورولا", callback_data="btn_motorola"),
        InlineKeyboardButton("⚡ استخراج زنده از هایترا", callback_data="btn_hytera")
    )
    
    bot.send_message(
        message.chat.id, 
        "🤖 به ربات اختصاصی **IMAN-BOT** خوش آمدید.\n\n"
        "این سیستم مستقیماً به سایت‌های مرجع متصل است. لطفاً هدف جستجو را انتخاب کنید:", 
        parse_mode="Markdown",
        reply_markup=markup
    )

# ۳. پردازش کلیک روی دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    back_markup = InlineKeyboardMarkup()
    back_markup.add(InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="btn_main"))

    if call.data == "btn_motorola":
        bot.answer_callback_query(call.id, "در حال اتصال...")
        bot.send_message(call.message.chat.id, "🔍 در حال جستجوی زنده در سرور Motorola Solutions...")
        res = search_radio_website("motorola")
        bot.send_message(call.message.chat.id, res, parse_mode="Markdown", reply_markup=back_markup)
        
    elif call.data == "btn_hytera":
        bot.answer_callback_query(call.id, "در حال اتصال...")
        bot.send_message(call.message.chat.id, "🔍 در حال جستجوی زنده در سرور Hytera...")
        res = search_radio_website("hytera")
        bot.send_message(call.message.chat.id, res, parse_mode="Markdown", reply_markup=back_markup)
        
    elif call.data == "btn_main":
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_welcome(call.message)

# ۴. تنظیمات ورودی وب‌هوک (تنظیمات استاندارد سرور رندر)
@app.route('/' + TOKEN, habits=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # آدرس اینترنتی پروژه شما در رندر به صورت خودکار جایگزین می‌شود
    render_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    bot.set_webhook(url=render_url)
    return "IMAN-BOT IS LIVE!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
