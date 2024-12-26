from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from app.data import SyncORM
from aiogram.types import Message


class SocialMediaCb(CallbackData, prefix='social'):
	smType: str


class CakeTypesCb(CallbackData, prefix="cakeTypeCb"):
	cakeType: str
	productId: int


class ChangeProfileCb(CallbackData, prefix='changeProfileCb'):
	needChange: str
	nameOfChange: str


class ChooseComponentCb(CallbackData, prefix='chooseComponentCb'):
	componentName: str
	componentTable: str


class ChooseComponentTypeCb(CallbackData, prefix='chooseComponentCb'):
	componentTypeName: str
      
class ChangeCallback(CallbackData, prefix='changeCallback'):
      pass


start = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Начать', callback_data='Start'),
											   InlineKeyboardButton(text='Отмена', callback_data='Cancel')]])

createNew = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да!', callback_data='CreateNew'),
												   InlineKeyboardButton(text='Нет(', callback_data='Cancel')]])

cakeOrNot = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Торт', callback_data='Cake'),
												   InlineKeyboardButton(text='Другое', callback_data='Another')]])

cancel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='Social_cancel')]])


# approve = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Подтвердить', callback_data='end_reg'),
# 												   InlineKeyboardButton(text='Исправить', callback_data='changeProfile')]])

skip1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Пропустить', callback_data='skip1')]])

approveProfile = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='changeProfileCancel')]])

webapp = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Открыть вебапп', web_app=WebAppInfo(url='https://bobr-ik.github.io/Conditer-s-bot/'))]])



async def social(inst='Не добавлено', vk='Не добавлено', yt='Не добавлено'):
	builder = InlineKeyboardBuilder()

	builder.button(
		text="YouTube:", callback_data=SocialMediaCb(smType='YouTube')
	)
	builder.button(
		text=yt, callback_data=SocialMediaCb(smType='YouTube')
	)
	builder.button(
		text="VK:", callback_data=SocialMediaCb(smType='VK')
	)
	builder.button(
		text=vk, callback_data=SocialMediaCb(smType='VK')
	)
	builder.button(
		text="Instagram:", callback_data=SocialMediaCb(smType='Instagram')
	)
	builder.button(
		text=inst, callback_data=SocialMediaCb(smType='Instagram')
	)
	builder.button(
		text='Продолжить', callback_data='approve'
	)
	builder.adjust(2)
	return builder.as_markup()


async def changeProfileKb():
	keyBoard = InlineKeyboardBuilder()
	keyBoard.button(text='Имя', callback_data=ChangeProfileCb(needChange='fname', nameOfChange='Имя'))
	keyBoard.button(text='Опыт работы', callback_data=ChangeProfileCb(needChange='fexp', nameOfChange='Опыт работы'))
	keyBoard.button(text='О себе', callback_data=ChangeProfileCb(needChange='fabout', nameOfChange='О себе'))
	keyBoard.button(text='Соцсети', callback_data='Social_cancel')
	keyBoard.button(text='Отмена', callback_data='approve')
	return keyBoard.adjust(1).as_markup()


async def createInlineCake(cakeTypes: list, productId: int):
	keyBoard = InlineKeyboardBuilder()
	for cake in cakeTypes:
		keyBoard.button(text=cake, callback_data=CakeTypesCb(cakeType=cake, productId=productId))
	keyBoard.add(InlineKeyboardButton(text='Другое', callback_data='cancel'))
	return keyBoard.adjust(2).as_markup()


async def cakeComponents(components: dict):
	keyBoard = InlineKeyboardBuilder()
	for key, value in components.items():
		keyBoard.button(text=key + ':', callback_data=ChooseComponentCb(componentName=key, componentTable=value))
		keyBoard.button(text=' ', callback_data=ChooseComponentCb(componentName=key, componentTable=value))
	keyBoard.button(text='Подтвердить', callback_data='Cancel')
	return keyBoard.adjust(2).as_markup()


async def cakeComponentTypes(componentTypes: list):
	keyBoard = InlineKeyboardBuilder()
	for value in componentTypes:
		keyBoard.button(text=value, callback_data=ChooseComponentTypeCb(componentTypeName=value))
	keyBoard.adjust(2)
	keyBoard.button(text='Подтвердить', callback_data='Cancel')
	return keyBoard.as_markup()


class Cake(CallbackData, prefix='cake'):
    action: str
    what: str
    dop: str
    index: str
    
class Cake_desc(CallbackData, prefix='cake_desc'):
	action: str


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
    kb.row(InlineKeyboardButton(text='Опубликовать торт ✅', callback_data=Cake(action='confirm_order', what= '', dop = '', index='').pack()))
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

def kb_for_approve():
      approve = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Подтвердить', callback_data='end_reg'),
										   InlineKeyboardButton(text='Исправить', callback_data=ChangeCallback().pack())]])
      return approve