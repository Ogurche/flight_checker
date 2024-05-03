from aiogram import types
from aiogram import Dispatcher
from aiogram.filters.command import Command

from sys_files.bot_creation import dp

async def start_cmd (message: types.Message):
    await message.answer('Бот для поиска авиабилетов')


async def register_info (dp:Dispatcher):
    dp.message.register(start_cmd,Command('start') )