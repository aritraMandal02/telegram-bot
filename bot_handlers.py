from telegram import ForceReply, Update
from helpers.imgfilter import image_filters
from helpers.random_quote import get_quote
from helpers.weather import get_weather
from telegram.ext import (Application,
                          CommandHandler,
                          ContextTypes,
                          MessageHandler,
                          filters,
                          ConversationHandler)


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


async def send_quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    quote = get_quote()
    quote = f"<b>Quote on {quote['category']}:</b>\n{quote['quote']}\n<i>— {quote['author']}</i>"
    await update.message.reply_text(quote, parse_mode='HTML')


async def send_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        weather = get_weather(' '.join(context.args))
        await update.message.reply_text(weather, parse_mode='HTML')
    else:
        await update.message.reply_text('Send `/weather city_name`', parse_mode='MarkdownV2')
