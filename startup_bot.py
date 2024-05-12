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

async def schedule_daily_task():
    while True:
        print ('date')
        await asyncio.sleep(5)

# Запуск процесса поллинга новых апдейтов
async def main():
    await register_info(dp)

    task2 = asyncio.create_task(dp.start_polling(bot, skip_update=True))
    task3 = asyncio.create_task(schedule_daily_task())
    print ('Бот запущен')
    # Wait for all tasks to complete

    await asyncio.gather(task2, task3)

if __name__ == '__main__':
    logging_bot()
    asyncio.run(main())
