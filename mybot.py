# -*- coding: utf-8 -*-
import telebot
from telebot import types
import time

BOT_TOKEN = "7901768407:AAECm7K05v7V3KzG_uVb33z-bT9aM_f-Ggo"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn = types.InlineKeyboardButton("🎁 باز کردن جعبه سوپرایز ایمان", callback_data="open_box")
    markup.add(btn)
    text = "سلام ایمان عزیز! 👋\n\nیک جعبه سوپرایز مرموز اینجاست... 📦✨\nروی دکمه زیر کلیک کن:"
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "open_box":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🔄 در حال اسکن کردن هویت شما... لطفاً منتظر بمانید...")
        time.sleep(1.5)
        surprise_text = "🎉🔴 **سوووووپرایزززززز!** 🔴🎉\n\n👑 ایمان عزیز، این ربات بدون نیاز به ترموکس گوشی شما و از قلب سرورهای قدرتمند زنده شده است! 🔓🧠"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=surprise_text, parse_mode="Markdown")

bot.infinity_polling()
