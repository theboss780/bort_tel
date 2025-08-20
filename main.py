import os
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

# =======================
# 1) قراءة المفاتيح من متغيرات البيئة
# =======================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# =======================
# 2) أوامر البوت
# =======================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً! 👋\nأنا بوت ChatGPT. أرسل لي أي رسالة وسأرد عليها."
    )

async def chatgpt_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_name = update.message.from_user.first_name

    # عرض حالة الكتابة
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}],
            max_tokens=500
        )
        reply_text = response.choices[0].message.content
        await update.message.reply_text(f"أهلاً {user_name} 👋\n\n{reply_text}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ خطأ: {str(e)}")

# =======================
# 3) معالج الأخطاء
# =======================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"🚨 خطأ: {context.error}")

# =======================
# 4) تشغيل البوت
# =======================
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt_reply))
    application.add_error_handler(error_handler)

    print("🚀 البوت شغال الآن!")
    application.run_polling()

if __name__ == "__main__":
    main()
