import logging
from aiogram import executor
from models.database import engine_develop
from views.telegram_usage import dp
from views.telegram_ui import *


if __name__ == "__main__":
    # Configure logging
    engine_develop()
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)