import telebot

TOKEN = "SIZNING_TOKENINGIZ"  # BotFather dan olingan token
bot = telebot.TeleBot(TOKEN)

# Savollar va javoblar ro‘yxati
questions = [
    ("5 + 7 = ?", "12"),
    ("9 - 4 = ?", "5"),
    ("6 × 3 = ?", "18"),
    ("20 ÷ 5 = ?", "4"),
    ("15 + 6 = ?", "21")
]

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {"index": 0, "correct": 0}
    bot.send_message(message.chat.id, "Salom! Matematika testini boshlaymiz.\n")
    ask_question(message.chat.id)

def ask_question(chat_id):
    idx = user_data[chat_id]["index"]
    if idx < len(questions):
        bot.send_message(chat_id, questions[idx][0])
    else:
        finish_test(chat_id)

@bot.message_handler(func=lambda m: m.chat.id in user_data)
def check_answer(message):
    chat_id = message.chat.id
    idx = user_data[chat_id]["index"]
    if idx < len(questions):
        if message.text.strip() == questions[idx][1]:
            user_data[chat_id]["correct"] += 1
        user_data[chat_id]["index"] += 1
        ask_question(chat_id)

def finish_test(chat_id):
    correct = user_data[chat_id]["correct"]
    total = len(questions)
    percent = (correct / total) * 100

    if 40 <= percent < 60:
        grade = "C"
    elif 60 <= percent < 75:
        grade = "C+"
    else:
        grade = "B yoki boshqa daraja"

    bot.send_message(chat_id, f"Siz {correct}/{total} ta to‘g‘ri javob berdingiz. "
                              f"Natija: {percent:.0f}%. Darajangiz: {grade}")
    del user_data[chat_id]

print("Bot ishga tushdi...")
bot.infinity_polling()
