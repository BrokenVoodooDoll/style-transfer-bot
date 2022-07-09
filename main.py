import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, \
    MessageHandler, filters
from style_transfer import style_transfer
from enum import Enum
import os.path as osp

class State(Enum):
    CHOOSING_CONTENT = 0
    CHOOSING_STYLE = 1

STATE = State.CHOOSING_CONTENT

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
        text="This bot transfers style from one photograph to another. \
Send me two photos: a content image and a style image. \
The order is important!")

async def download_image(update: Update, img_name: str):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    await file.download(img_name)
    return photo['height']

async def transfer_style(update: Update, context: ContextTypes.DEFAULT_TYPE, img_height):
    output_img = style_transfer("content.jpg", "style.jpg", img_height)
    
    with open(output_img, 'rb') as im:
        await context.bot.send_photo(chat_id=update.effective_chat.id,
            photo=im)

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global STATE

    img_root = "neural_style_transfer/data"
    content_img = osp.join(img_root, "content-images/content.jpg")
    style_img = osp.join(img_root, "style-images/style.jpg")
    img_height = 400
    if STATE == State.CHOOSING_CONTENT:
        img_height = await download_image(update, content_img)
        STATE = State.CHOOSING_STYLE
    elif STATE == State.CHOOSING_STYLE:
        STATE = State.CHOOSING_CONTENT
        await download_image(update, style_img)
        await context.bot.send_message(chat_id=update.effective_chat.id,
            text="Please wait. This may take a while...")   
        await transfer_style(update, context, img_height)

if __name__ == '__main__':
    with open('token.txt', 'rt') as f:
        api_token = f.readline()

    application = ApplicationBuilder().token(api_token).build()
    
    help_handler = CommandHandler('help', help)
    photo_handler = MessageHandler(filters.PHOTO & (~filters.COMMAND), image)
    
    application.add_handler(help_handler)
    application.add_handler(photo_handler)
    
    application.run_polling()