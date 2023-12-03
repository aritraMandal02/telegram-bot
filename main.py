import logging
from dotenv import load_dotenv
import os
from experiments import *
from bot_handlers import *

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler("imgfilter", choose_filter))
    application.add_handler(MessageHandler(filters.PHOTO, apply_filter))
    application.add_handler(CommandHandler("quote", send_quote))
    application.add_handler(CommandHandler("weather", send_weather))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
