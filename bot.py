import os
from typing import Final

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

from response_handler import handle_response
from create_food_command import conv
from today_command import today_command
from errors import TelegramBotTokenError

BOT_USERNAME: Final = "@szafarzbot"
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise TelegramBotTokenError("TELEGRAM_BOT_TOKEN is not set") 

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_response(update, context)
    await update.message.reply_text(response)

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(conv)
    app.add_handler(CommandHandler("today", today_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # START THE BOT
    app.run_polling()