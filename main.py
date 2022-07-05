import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from PIL import Image
from style_transfer import style_transfer
from enum import Enum


class State(Enum):
    IDLE = 0
    CHOOSING_CONTENT = 1
    CHOOSING_STYLE = 2

state = State

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
        text="This bot transfers style from one photograph to another. \
        Send me two photos: a content image and a style image. \
        The order is important!")

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.photo)

    file = await update.message.photo[-1].get_file()
    await file.download("./photo.jpeg")

    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait. This may take a while...")
    # await style_transfer('figures.jpg', 'vg_starry_night.jpg')
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Got it")


if __name__ == '__main__':
    with open('token.txt', 'rt') as f:
        api_token = f.readline()

    application = ApplicationBuilder().token(api_token).build()
    
    help_handler = CommandHandler('help', help)
    photo_handler = MessageHandler(filters.PHOTO & (~filters.COMMAND), image)
    
    application.add_handler(help_handler)
    application.add_handler(photo_handler)
    
    application.run_polling()