import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from PIL import Image

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send an image to me")

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    await file.download("./photo.jpeg")

    # here the network starts
    

if __name__ == '__main__':
    with open('token.txt', 'rt') as f:
        api_token = f.readline()

    application = ApplicationBuilder().token(api_token).build()
    
    help_handler = CommandHandler('help', help)
    photo_handler = MessageHandler(filters.PHOTO & (~filters.COMMAND), image)
    
    application.add_handler(help_handler)
    application.add_handler(photo_handler)
    
    application.run_polling()