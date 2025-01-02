from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, callback_data
from aiogram.types import Message, CallbackQuery
import user_bot.keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from user_bot.keyboards import Cake
from app.data import SyncORM
from config import settings
# from user_bot.dop_file import user_bot as bot
# from collections import defauldict
chat_id = 0

rt = Router()
bot = Bot(token=settings.USER_BOT_TOKEN)


class Order(StatesGroup):
    cake_type = State()
    cake_type_back = State()
    cake_ins = State()
    cake_ins_back = State()


def dict_to_text(data):
    s = ''
    for elem in data.items():
        s += f'{elem[0]}: {elem[1][0] if elem[1][0] != 1 else 'Не выбрано'}\n\n'
    return s

def order_desc(data):
    text=f"\n\nТип вышего торта: {data['cake_type']}\n\nВкусы ингридиентов:\n"
    text += dict_to_text(data['cake_ins'])
    return text


@rt.message(CommandStart())
async def start(message: Message):
    global chat_id
    chat_id = message.chat.id
    await message.answer("Здравствуйте! В этом телеграм боте вы с лёгкостью сможете найти кондитерское решение вашего вопроса)", reply_markup=kb.mainkb, parse_mode='HTML')
    # await bot.send_message(chat_id=chat_id, text="Для начала выберите тип торта.", reply_markup=kb.cake_type_kb(), parse_mode='HTML')


@rt.callback_query(F.data == 'cakes')
async def cakes(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Для начала выберите тип торта.", reply_markup=kb.cake_type_kb(), parse_mode='HTML')


@rt.callback_query(Cake.filter(F.action == 'cake_type'))
async def add_cake_type(callback: CallbackQuery, callback_data: Cake, state: FSMContext):
    data = {}
    dop = {}
    for elem in SyncORM.get_cake_ingrs(callback_data.what):
        data[elem] = []
        dop[elem] = []
    await state.update_data(cake_type=callback_data.what, cake_type_back=callback_data.index, cake_ins=data, cake_ins_back=dop)
    await callback.answer()
    # print(callback_data.what)
    await callback.message.edit_text(text='Приступим к выбору начинок для ингридиентов.', reply_markup=kb.cake_ingrs_kb(callback_data.what, (await state.get_data())['cake_ins']))


@rt.callback_query(Cake.filter(F.action == 'elems'))
async def add_cake_ingr_taste(callback: CallbackQuery, callback_data: Cake, state: FSMContext):
    await callback.message.edit_text(text='Выберите вкусы ингридиента.', reply_markup=kb.cake_ingr_tastes_kb(callback_data.dop, callback_data.what, (await state.get_data())['cake_ins'][f'{callback_data.what}']), parse_mode='HTML')
    await callback.answer()


@rt.callback_query(Cake.filter(F.action == 'tastes'))
async def add_to_order_ingrs_taste(callback: CallbackQuery, callback_data: Cake, state: FSMContext):
    data = (await state.get_data())['cake_ins']
    dop = (await state.get_data())['cake_ins_back']
    if callback_data.what in data[callback_data.dop]:
        data[callback_data.dop].pop(data[callback_data.dop].index(callback_data.what))
        dop[callback_data.dop].pop(dop[callback_data.dop].index(callback_data.index))
    else:
        data[callback_data.dop].append(callback_data.what)
        dop[callback_data.dop].append(callback_data.index)
    await state.update_data(cake_ins=data, cake_ins_back=dop)
    await callback.answer()
    await callback.message.edit_text(text='Выберите вкусы ингридиента.', reply_markup=kb.cake_ingr_tastes_kb((await state.get_data())['cake_type'], callback_data.dop, (await state.get_data())['cake_ins'][f'{callback_data.dop}']), parse_mode='HTML')



@rt.callback_query(Cake.filter(F.action == 'confirm_tastes'))
async def confirm_ingrs_taste(callback: CallbackQuery, callback_data: Cake, state: FSMContext):
    await callback.message.edit_text(text='Продолжайте выбор начинок соответствующих ингридиентов. По завершении нажмите кнопку \n"Подтвердить заказ  ✅".', reply_markup=kb.cake_ingrs_kb((await state.get_data())['cake_type'], (await state.get_data())['cake_ins']), parse_mode='HTML')
    await callback.answer()


@rt.callback_query(Cake.filter(F.action=='confirm_order'))
async def confirm_order(callback: CallbackQuery, callback_data: Cake, state: FSMContext):
    await callback.answer()
    print((await state.get_data()))
    print(SyncORM.get_tastes_id((await state.get_data())))

