from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import callback_data
from app.data import SyncORM
from aiogram.filters.callback_data import CallbackData


class Cake(CallbackData, prefix='cake'):
    action: str
    what: str
    dop: str
    index: str


def add_tastes_to_main_kb(tastes: list, kb: InlineKeyboardBuilder, ingr, cake_type):
    if len(tastes) % 2 == 1:
        k = len(tastes) - 1
    else:
        k = len(tastes)
    for i in range(0, k, 2):
        kb.row(
                InlineKeyboardButton(text=tastes[i], callback_data=Cake(action='elems', what=str(ingr),dop=str(cake_type), index='').pack()),
                InlineKeyboardButton(text=tastes[i + 1], callback_data=Cake(action='elems', what=str(ingr), dop=str(cake_type), index= '').pack())
            )
    if len(tastes) % 2 == 1:
        kb.row(
            InlineKeyboardButton(text=tastes[-1], callback_data=Cake(action='elems', what=str(ingr),dop=str(cake_type), index='').pack()),
            InlineKeyboardButton(text='➕ Добавить вкус', callback_data=Cake(action='elems', what=str(ingr),dop=str(cake_type), index='').pack())
        )
    else:
        kb.row(InlineKeyboardButton(text='➕ Добавить вкус', callback_data=Cake(action='elems', what=str(ingr),dop=str(cake_type),index='').pack()))
    return kb


def pars(data):
    data = data[1:len(data) - 1].replace("'", '')
    return data.split(', ')


mainkb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Торты', callback_data='cakes')],
])


def update(clas, *args):
    for elem in args:
        clas.elem[0] = elem[1]
    return clas


def cake_type_kb():
    kb = InlineKeyboardBuilder()
    for elem in SyncORM.get_cake_types():
        kb.add(InlineKeyboardButton(text=str(elem[0]), callback_data=Cake(action='cake_type', what=str(elem[0]), dop='', index=f'{elem[1]}').pack()))
    return kb.adjust(2).as_markup()


def cake_ingrs_kb(cake_type, tastes):
    kb = InlineKeyboardBuilder()
    for elem in SyncORM.get_cake_ingrs(cake_type):
        kb.row(
            InlineKeyboardButton(text=f'==={str(elem).upper()}===', callback_data=Cake(action='elems', what=f'{elem}', dop=str(cake_type), index='').pack())
            )
        kb = add_tastes_to_main_kb(tastes[elem], kb, elem, cake_type)
    kb.row(InlineKeyboardButton(text='Подтвердить заказ ✅', callback_data=Cake(action='confirm_order', what= '', dop = '', index='').pack()))
    return kb.as_markup()


def cake_ingr_tastes_kb(cake_type, cake_ingr, t_tastes):
    kb = InlineKeyboardBuilder()
    for elem in SyncORM.getcake_ingr_taste(cake_type, cake_ingr):
        if elem[0] in t_tastes:
            kb.add(InlineKeyboardButton(text='✅' + str(elem[0]), callback_data=Cake(action='tastes', what=f'{elem[0]}', dop=str(cake_ingr), index=str(elem[1])).pack()))
        else:
            kb.add(InlineKeyboardButton(text=str(elem[0]), callback_data=Cake(action='tastes', what=f'{elem[0]}', dop=str(cake_ingr), index=str(elem[1])).pack()))
    kb.row(InlineKeyboardButton(text='Подтвердить ✅', callback_data=Cake(action='confirm_tastes', what=f'{cake_ingr}', dop = str(cake_ingr), index='').pack()))
    return kb.adjust(2).as_markup()
