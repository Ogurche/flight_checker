from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')

storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
dp= Dispatcher (bot, storage= storage)