import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from dotenv import load_dotenv
import os
from experiments import *

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


async def send_creater_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_document(document='https://python-telegram-bot.org/static/testfiles/telegram.gif')


async def choose_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        reply = "These are the filters I can apply:\n"
        for filter in image_filters.keys():
            reply += f'`/imgfilter {filter}`\n'
        reply += "Click and copy any of the above filters and send to apply\."
        await update.message.reply_text(reply, parse_mode='MarkdownV2')
    if context.args:
        if context.args[0] in image_filters.keys():
            context.user_data['filter'] = context.args[0]
            await update.message.reply_text(f"Ok send the image. {context.user_data['filter']} filter will be applied.")
        else:
            await update.message.reply_text(f"Sorry, I don't know about {context.args[0]} filter.")

async def apply_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('filter'):
        image = await update.message.effective_attachment[-1].get_file()
        await update.message.reply_text("Image Uploaded! Applying the filter. Please wait...")
        img_arr = await image.download_as_bytearray()
        processed_img = image_filters[context.user_data['filter']](img_arr)
        await update.message.reply_photo(photo=processed_img)
        del context.user_data['filter']


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cp", send_creater_photo))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler('imgfilter', choose_filter))
    application.add_handler(MessageHandler(filters.PHOTO, apply_filter))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
