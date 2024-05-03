# Запуск бота 

import logging 
from aiogram import Dispatcher
from aiogram import types
import asyncio
from handler.info_save import register_info

from sys_files.bot_creation import dp, bot

# logging to file with time 
def logging_bot():
    logging.basicConfig(level= logging.INFO 
                        ,filename='bot.log'
                        , format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.warning ('Bot started')

# # Хэндлер на команду /start
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Hello!")

# Запуск процесса поллинга новых апдейтов
async def main():
    await register_info(dp)
    await dp.start_polling(bot,skip_update=True)

if __name__ == '__main__':
    logging_bot()
    asyncio.run(main())