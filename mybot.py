import telebot

TOKEN = "8642386388:AAEhGZn73Coiv6bNysv96Jxya4SSb73fw2E"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام مانوئل جان! ربات با موفقیت بیدار شد و دارد کار می‌کند. 🚀")

bot.infinity_polling()
