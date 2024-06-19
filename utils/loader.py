from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage

BOT_TOKEN = '6349365100:AAEyanEQju5dX2oVuw2XGdLpVyzVDf2H6nI'

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher(bot, storage=storage)
