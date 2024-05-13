from aiogram import types
from aiogram import Dispatcher, html, F
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from sys_files.bot_creation import dp, bot
from checker.db_adapter import DbConnection, db_usage

# yes_no = ['Да','Нет']

class User_request(StatesGroup):
    full_request = State()

async def start_cmd (message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}\nЭто бот для поиска авиабилетов')

async def get_request(message:types.Message, state: FSMContext):
    await message.answer('Введите запрос\n\n'
                         f"Вид запроса\n{html.underline(html.bold('Откуда'))},"
                         f"{html.underline(html.bold('Куда'))},"
                         f"{html.underline(html.bold('Когда (дд.мм.гггг)'))}"
                         "\n(параметры через запятую )", parse_mode= ParseMode.HTML)
    await state.set_state(User_request.full_request)

async def request_validation(message:types.Message, state: FSMContext):
    #TODO: Text validation
    # 1. If have incorrect number of params send message
    departure_from , arrival_at , date = map(str.strip, message.text.split(','))
    data_dict = {'origin': departure_from, 'destination': arrival_at, 'dep_date': date, 'user_id':message.from_user.id}
    
    #TODO: Make validation
    # 1. Departure. db_adabter.db_usage.decode() (return list or None)
    # 2. Arrival db_adabter.db_usage.decode() (return list or None)
    # 3. Date date > curdate, date format is dd.mm.yyyy: re.match(r'^\d{2}\.\d{2}\.\d{4}$', date)
    # 4. Check NUll

    await state.update_data(data=data_dict)
    await message.answer(f'Ваш запрос: {departure_from}\n{arrival_at}\n{date}')

    #TODO: Make keybord
    await message.answer(f'Вы уверены, что хотите отправить запрос?\n'
                         f'{html.bold("Да")}\n'
                         f'{html.bold("Нет")}', parse_mode= ParseMode.HTML)

async def requesr_agree (message:types.Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer('Запрос сохранен')
        #TODO: SAVE data   
        saver = db_usage(DbConnection)    
        data_dict = await state.get_data()
        saver.save_request(data_dict)
        # DbConnection.
        await state.clear()
    if message.text == 'Нет':
        await message.answer('Повторите запрос')
        await get_request(message, state)

#TODO: Cancel button 

async def simple_answer(message:types.Message):
    await message.answer('Dayte denyg')

async def register_info (dp:Dispatcher):
    dp.message.register(start_cmd,Command('start') )
    dp.message.register(get_request,Command('request') )
    dp.message.register(requesr_agree,User_request.full_request, F.text.in_({"Да", "Нет"}))
    dp.message.register(request_validation,User_request.full_request)
    # Сюда надо еще накидать хендлеров 
    #
    #
    dp.message.register(simple_answer)