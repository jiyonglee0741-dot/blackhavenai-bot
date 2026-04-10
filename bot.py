import os
import anthropic
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8685122003:AAGutrT_gpf_Euep9dioNHFPDuh2zcceJ2Q")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
conversation_history = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "안녕하세요! 저는 GOO AI 봇이에요 🤖\n무엇이든 물어보세요!\n\n/reset - 대화 초기화")

@bot.message_handler(commands=['reset'])
def reset(message):
    user_id = message.from_user.id
    conversation_history[user_id] = []
    bot.reply_to(message, "대화가 초기화됐어요! 새로 시작해요 😊")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    user_text = message.text
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({"role": "user", "content": user_text})
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system="당신은 친절하고 유능한 AI 어시스턴트입니다. 한국어로 대화해주세요.",
            messages=conversation_history[user_id]
        )
        reply = response.content[0].text
        conversation_history[user_id].append({"role": "assistant", "content": reply})
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"오류가 발생했어요 😢\n{str(e)}")

print("🤖 GOO AI 봇 시작!")
bot.polling(none_stop=True)
