from aiogram import Bot
import logging
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружены, так как отсутствует файл .env')
else:
    load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
YOOKassa = os.getenv('YOOTOKEN')
YOUR_CHAT_ID = os.getenv('TELEGRAM_ID')
NICKNAME_BOT = os.getenv('BOT_NICKNAME')
GOOGLE = os.getenv('GOOGLE_SHEET')
PASSWORD_YANDEX_ENV = os.getenv('PASSWORD_YANDEX')


logging.basicConfig(level=logging.INFO)
logger_name = 'image_bot'
logger = logging.getLogger(logger_name)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)



