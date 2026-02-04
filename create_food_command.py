from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
import re
from database import get_connection
from food_repository import create_food_record, food_exists
NAME, CALORIES, PROTEIN, FAT, CARBS, CONFIRMATION = range(6)

pattern = re.compile(r'^\d+(?:[.,]\d+)?g?$')
def parse_number_input(text: str) -> float:
    return float(text.replace(",", ".").replace("g", ""))

async def createfood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Name: ")
    return NAME

async def food_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with get_connection() as conn:
        if food_exists(conn, update.message.text.lower()):
            await update.message.reply_text("Food with this name already exists. You can edit it with /editfood.")
            context.user_data.clear()
            return ConversationHandler.END

    context.user_data['name'] = update.message.text.lower()
    await update.message.reply_text("Calories per 100g: ")
    return CALORIES

async def food_calories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pattern.fullmatch(update.message.text):
        await update.message.reply_text("Please enter a valid number for calories.")
        return CALORIES

    context.user_data['calories'] = parse_number_input(update.message.text)
    await update.message.reply_text("Protein per 100g: ")
    return PROTEIN

async def food_protein(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pattern.fullmatch(update.message.text):
        await update.message.reply_text("Please enter a valid number for protein.")
        return PROTEIN

    context.user_data['protein'] = parse_number_input(update.message.text)
    await update.message.reply_text("Fat per 100g: ")
    return FAT

async def food_fat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pattern.fullmatch(update.message.text):
        await update.message.reply_text("Please enter a valid number for fat.")
        return FAT
    
    context.user_data['fat'] = parse_number_input(update.message.text)
    await update.message.reply_text("Carbs per 100g: ")
    return CARBS

async def food_carbs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pattern.fullmatch(update.message.text):
        await update.message.reply_text("Please enter a valid number for carbs.")
        return CARBS
    
    context.user_data['carbs'] = parse_number_input(update.message.text)

    await update.message.reply_text(
        f"Do you want to add this food?\n"
        f"Food: {context.user_data['name']}\n"
        f"Calories per 100g: {context.user_data['calories']}\n"
        f"Protein per 100g: {context.user_data['protein']}\n"
        f"Fat per 100g: {context.user_data['fat']}\n"
        f"Carbs per 100g: {context.user_data['carbs']}\n"
    )

    return CONFIRMATION

async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text in ['yes', 'y', 'confirm', "tak", 't']:
        with get_connection() as conn:
            create_food_record(
                conn,
                context.user_data['name'],
                context.user_data['calories'],
                context.user_data['protein'],
                context.user_data['fat'],
                context.user_data['carbs'],
            )
        await update.message.reply_text("Food added successfully.")
    else:
        await update.message.reply_text("Food creation cancelled.")
    
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Clean up any temporary state
    context.user_data.clear()

    await update.message.reply_text(
        "Operation cancelled."
    )

    return ConversationHandler.END

conv = ConversationHandler(
    entry_points=[CommandHandler("createfood", createfood)],

    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, food_name)],
        CALORIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, food_calories)],
        PROTEIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, food_protein)],
        FAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, food_fat)],
        CARBS: [MessageHandler(filters.TEXT & ~filters.COMMAND, food_carbs)],
        CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmation)],
    },     

    fallbacks=[CommandHandler("cancel", cancel)],
)
