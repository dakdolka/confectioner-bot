from aiogram import F, Router, Bot
from config import settings
from typing import Union, Dict, Any
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import Message, CallbackQuery, WebAppData
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.data import SyncORM
import conf_bot.keyboards as kb
import json
# from DataBase import cursor, db


	

TypesDict = {
	'Cake': {
		'Муссовый': {
			'Начинка': {'Яблочная': 'end', 'Лимонная': 'end'},
			'Мусс': {'Черничный': 'end', 'Смородиновый': 'end'}
		},
		'Бисквитный': {
			'Бисквит': {'a': 'end', 'b': 'end'},
			'начинка': {'a': 'end', 'c': 'end'}
		}
	},
	'Another': {}}

cakeTypesTag = 'cakes_types_'
router = Router()
bot = Bot(token=settings.CONF_BOT_TOKEN)


class Reg(StatesGroup):
	name = State()
	exp = State()
	aboutCond = State()
	VK = State()
	YouTube = State()
	Instagram = State()
	changeName = State()
	changeExp = State()
	changeAbout = State()
	approve_text = State()
	approve_mes_id = State()
	photo = State()

class Cake(StatesGroup):
	name = State()
	weight = State()
	filling = State()
	newType = State()
	newType2 = State()

def build_approve(data):
	text = f'''
Подтвердите данные профиля:
Имя: {data.get("fname", "Не указано")}
Опыт работы: {data.get("fexp", "Не указано")}
О себе: {data.get("fabout", "Не указано")}

СОЦСЕТИ

Youtube: {data.get("fyoutube", "Не указано")}
VK: {data.get("fvk", "Не указано")}
Instagram: {data.get("finstagram", "Не указано")}'''
	return text


@router.message(CommandStart())
async def cmd_start(message: Message):
	userid = message.from_user.id
	conf = SyncORM.get_conditer_info(userid)
	print(conf)
	if conf:
		await message.answer(text=f'Здравствуйте, {conf['name']}! Чем займёмся?', reply_markup=kb.createNew)
	else:
		await message.answer('======Добро пожаловать!!=======\nЗаполните анкету', reply_markup=kb.start)
  
@router.callback_query(F.data == 'myCakes')
async def myCakes(callback: CallbackQuery):
	await callback.answer()
	pass

class WebAppDataFilter(Filter):
	async def __call__(self, message: Message, **kwargs) -> Union[bool, Dict[str, Any]]:
		return dict(web_app_data=message.web_app_data) if message.web_app_data else False

#... Инициализация бота

@router.message(WebAppDataFilter())
async def handle_web_app_data(message: Message, web_app_data: WebAppData):
	diiict = json.loads(web_app_data.data)
	await message.answer("Received web app data: " + ' '.join(map(str, list(diiict.values()))))


@router.callback_query(F.data == 'Cancel')
async def cancel(callback: CallbackQuery):
	await callback.answer()
	await callback.message.edit_text('Ну и иди гуляй')


@router.callback_query(F.data == 'Start')
async def start(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.edit_text(text='Введите Имя:')
	await state.set_state(Reg.name)


@router.message(Reg.name)
async def name(message: Message, state: FSMContext):
	await state.update_data(fname=message.text)
	await state.set_state(Reg.exp)
	await message.answer(text='Ваш опыт работы:')


@router.message(Reg.exp)
async def exp(message: Message, state: FSMContext):
	userid = message.from_user.id
	print(userid)
	await state.set_state(Reg.photo)
	await message.answer(text='Аватарка вашего профиля', reply_markup=kb.skip1)
	await state.update_data(fexp=message.text)
 
@router.message(Reg.photo)
async def photo(message: Message, state: FSMContext):
	await state.update_data(fphoto=message.photo[0].file_id)
	print(message.photo[0].file_id)
	# await message.answer_photo(message.photo[0].file_id)
	await state.set_state(Reg.aboutCond)
	await message.answer(text='Расскажите о себе:', reply_markup=kb.skip2)


@router.callback_query(F.data == 'skip2')
async def add_social1(callback: CallbackQuery, state: FSMContext):
	await state.update_data(fabout='')
	await callback.message.edit_text(text='Добавьте свои социальные сети', reply_markup=await kb.social())
 
@router.callback_query(F.data == 'skip1')
async def add_social2(callback: CallbackQuery, state: FSMContext):
	await state.update_data(fphoto='')
	await callback.message.edit_text(text='РАсскажите о себе:', reply_markup=await kb.skip2())


@router.message(Reg.aboutCond)
async def add_social(message: Message, state: FSMContext):
	await state.update_data(fabout=message.text)
	await message.answer(text='Добавьте свои социальные сети', reply_markup=await kb.social())


@router.callback_query(F.data == 'Social_cancel')
async def social_cancel(callback: CallbackQuery, state: FSMContext):
	data = dict(await state.get_data())
	await callback.message.edit_text(text='Добавьте свои социальные сети', reply_markup=await kb.social(yt=data.get('fyoutube', 'Не добавлено'), vk=data.get('fvk', 'Не добавлено'), inst=data.get('finstagram', 'Не добавлено')))


@router.message(Reg.YouTube)
async def add_social_2(message: Message, state: FSMContext):
	await state.update_data(fyoutube=message.text)
	data = dict(await state.get_data())
	await message.answer(text='Ссылка успешно добавлена! хотите добавить еще?', reply_markup=await kb.social(yt=data.get('fyoutube', 'Не добавлено'), vk=data.get('fvk', 'Не добавлено'), inst=data.get('finstagram', 'Не добавлено')))


@router.message(Reg.VK)
async def add_social_2(message: Message, state: FSMContext):
	await state.update_data(fvk=message.text)
	data = dict(await state.get_data())
	await message.answer(text='Ссылка успешно добавлена! хотите добавить еще?', reply_markup=await kb.social(yt=data.get('fyoutube', 'Не добавлено'), vk=data.get('fvk', 'Не добавлено'), inst=data.get('finstagram', 'Не добавлено')))


@router.message(Reg.Instagram)
async def add_social_2(message: Message, state: FSMContext):
	await state.update_data(finstagram=message.text)
	data = dict(await state.get_data())
	await message.answer(text='Ссылка успешно добавлена! хотите добавить еще?', reply_markup=await kb.social(yt=data.get('fyoutube', 'Не добавлено'), vk=data.get('fvk', 'Не добавлено'), inst=data.get('finstagram', 'Не добавлено')))


@router.callback_query(kb.SocialMediaCb.filter())
async def add_social_link(callback: CallbackQuery, state: FSMContext, callback_data: kb.SocialMediaCb):
	await callback.answer()
	if callback_data.smType == 'YouTube':
		await state.set_state(Reg.YouTube)
	elif callback_data.smType == 'VK':
		await state.set_state(Reg.VK)
	elif callback_data.smType == 'Instagram':
		await state.set_state(Reg.Instagram)
	await callback.message.edit_text(text=f'Отправьте ссылку на Ваш {callback_data.smType}', reply_markup=kb.cancel)
 
 


@router.callback_query(F.data == 'approve')
async def approve(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	data = dict(await state.get_data())
	approve_text = build_approve(data)
	await state.update_data(approve_text=approve_text)
	await state.update_data(approve_mes_id=callback.message)
	await callback.message.edit_text(text=dict(await state.get_data())['approve_text'],
									 reply_markup=kb.kb_for_approve())


#  await bot.edit_message_text(f'Отправьте название и исполнителя желаемого трека. Как закончите - нажмите кнопку "Подтвердить✅"! \n\n{message_edit_for_songs(data, False)}', chat_id=message.chat.id, message_id=data['song_list_id'], reply_markup=kb_confirm_for_name)
@router.callback_query(kb.ChangeCallback.filter())
async def choose_change(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await bot.edit_message_text(f'{build_approve(dict(await state.get_data()))}\n\nЧто вы хотите исправить?',
							chat_id=callback.message.chat.id,
							message_id=callback.message.message_id, 
							reply_markup=await kb.changeProfileKb())
	# await callback.message.answer(text='Что вы хотели бы исправить?', reply_markup=await kb.changeProfileKb())


@router.callback_query(F.data == 'changeProfileCancel')
async def choose_change(callback: CallbackQuery):
	await callback.answer()
	await callback.message.edit_text(text='Что вы хотели бы исправить?', reply_markup=await kb.changeProfileKb())


@router.callback_query(kb.ChangeProfileCb.filter())
async def change_data(callback: CallbackQuery, callback_data: kb.ChangeProfileCb, state: FSMContext):
	await callback.answer()
	await callback.message.edit_text(text=f'======={callback_data.nameOfChange}=======\n\nВведите новые данные.\nРанее введенный текст:\n{dict(await state.get_data()).get(callback_data.needChange)}', reply_markup=kb.approveProfile)
	if callback_data.needChange == 'fname':
		await state.set_state(Reg.changeName)
	elif callback_data.needChange == 'fexp':
		await state.set_state(Reg.changeExp)
	elif callback_data.needChange == 'fabout':
		await state.set_state(Reg.changeAbout)


@router.message(Reg.changeName)
async def changeName(message: Message, state: FSMContext):
	await state.update_data(fname=message.text)
	data = dict(await state.get_data())
	await bot.delete_message(message.chat.id, message.message_id)
	await bot.edit_message_text(
		text=build_approve(data),
		chat_id=data['approve_mes_id'].chat.id,
		message_id=data['approve_mes_id'].message_id,
		reply_markup=kb.kb_for_approve())


@router.message(Reg.changeExp)
async def changeName(message: Message, state: FSMContext):
	await state.update_data(fexp=message.text)
	data = dict(await state.get_data())
	await bot.delete_message(message.chat.id, message.message_id)
	await bot.edit_message_text(
		text=build_approve(data),
		chat_id=data['approve_mes_id'].chat.id,
		message_id=data['approve_mes_id'].message_id,
		reply_markup=kb.kb_for_approve())


@router.message(Reg.changeAbout)
async def changeName(message: Message, state: FSMContext):
	await state.update_data(fabout=message.text)
	data = dict(await state.get_data())
	await bot.delete_message(message.chat.id, message.message_id)
	await bot.edit_message_text(
		text=build_approve(data),
		chat_id=data['approve_mes_id'].chat.id,
		message_id=data['approve_mes_id'].message_id,
		reply_markup=kb.kb_for_approve())


@router.callback_query(F.data == 'end_reg')
async def end_reg(callback: CallbackQuery, state: FSMContext):
	regData = dict(await state.get_data())
	await state.clear()
	yt = regData.get('fyoutube', '')
	vk = regData.get('fvk', '')
	inst = regData.get('finstagram', '')
	SyncORM.create_profile(*tuple([callback.from_user.id] + list(regData.values())[:3] + [yt, vk, inst]))
	await callback.message.edit_text(text='Регистрация успешно завершена! Хотите создать свой первый продукт?',
						 reply_markup=kb.createNew)


# @router.callback_query(F.data == 'CreateNew')  # Выбор торт или что-то другое
# async def create(callback: CallbackQuery):
# 	await callback.message.answer(text='Какое творение вы хотите создать?', reply_markup=kb.cakeOrNot)
# 	await callback.answer()


# @router.callback_query(F.data == 'Cake')  # Выбор типа торта
# async def createCake1(callback: CallbackQuery):
	# request = f'SELECT fproductid FROM tproducttype'
	# cursor.execute(request)
	# fproductid = max(list(map(lambda x: x[0], cursor.fetchall())) or [-1]) + 1

	# request = f'INSERT INTO tproductType (fcreator, ftypeName, fproductid) VALUES ({callback.from_user.id}, "cake", {fproductid})'
	# cursor.execute(request)
	# db.commit()

	# request = f"SELECT fcaketypes FROM tcaketypes"
	# cursor.execute(request)
	# cakeTypes = list(map(lambda x: x[0], cursor.fetchall()))
	# print(cakeTypes)

	# cakeTypes = SyncORM.get_cake_types()
	# await callback.answer()
	# await callback.message.edit_text(text='Какого вида будет ваш торт?', reply_markup=await kb.createInlineCake(cakeTypes))


# @router.callback_query(kb.CakeTypesCb.filter())
# async def add_social_link(callback: CallbackQuery, callback_data: kb.CakeTypesCb):
# 	await callback.answer()
# 	request = f'INSERT INTO ttort (fproductId, ftypename) VALUES ({callback_data.productId}, "{callback_data.cakeType}")'
# 	cursor.execute(request)
# 	db.commit()

# 	request = f'SELECT fcakecomponents FROM tcakecomponents WHERE ftypename LIKE "{callback_data.cakeType}"'
# 	cursor.execute(request)
# 	components = dict(map(lambda x: (x.split(',')[0], x.split(',')[1]), list(cursor.fetchall())[0][0].split(';')))
# 	print(components)
# 	await callback.message.edit_text(text='Выберить компоненты торта', reply_markup=await kb.cakeComponents(components))


# @router.callback_query(kb.ChooseComponentCb.filter())
# async def choose_component(callback: CallbackQuery, callback_data: kb.ChooseComponentCb):
# 	await callback.answer()
# 	request = f'SELECT fname FROM {callback_data.componentTable}'
# 	cursor.execute(request)
# 	componentTypes = list(map(lambda x: x[0], cursor.fetchall()))
# 	print(componentTypes)
# 	await callback.message.edit_text(text=f'Выберите компонент {callback_data.componentName} для вашего торта', reply_markup=await kb.cakeComponentTypes(componentTypes))


# @router.message(CommandStart())
# async def ans(message: Message):
#     await message.answer(text='hyiasgugtdgasys')

#создание торта
class Order(StatesGroup):
    cake_type = State()
    cake_type_back = State()
    cake_ins = State()
    cake_ins_back = State()
    cake_desc = State()
    cake_name = State()


def dict_to_text(data):
    s = ''
    for elem in data.items():
        s += f'{elem[0]}: {elem[1][0] if elem[1][0] != 1 else 'Не выбрано'}\n\n'
    return s

def order_desc(data):
    text=f"\n\nТип вышего торта: {data['cake_type']}\n\nВкусы ингридиентов:\n"
    text += dict_to_text(data['cake_ins'])
    return text

@router.callback_query(F.data == 'CreateNew')
async def cakes(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await state.set_state(Order.cake_name)
	await callback.message.edit_text("Для начала Введите название вашего торта.")

@router.message(Order.cake_name)
async def handle_cake_name(message: Message, state: FSMContext):
	await state.update_data(cake_name=message.text)
	await message.answer(f"Название торта: {message.text}\n Теперь введите описание!")
	await state.set_state(Order.cake_desc)

@router.message(Order.cake_desc)
async def handle_cake_name(message: Message, state: FSMContext):
	await state.update_data(cake_desc=message.text)
	dop = await state.get_data()
	await message.answer(f"Название торта: <b>{dop['cake_name']}</b>\n Описание: {dop['cake_desc']}\n Выберите тип вашего торта.", reply_markup=kb.cake_type_kb(), parse_mode='HTML')

@router.callback_query(kb.Cake.filter(F.action == 'cake_type'))
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


@router.callback_query(kb.Cake.filter(F.action == 'elems'))
async def add_cake_ingr_taste(callback: CallbackQuery, callback_data: Cake, state: FSMContext):
    await callback.message.edit_text(text='Выберите вкусы ингридиента.', reply_markup=kb.cake_ingr_tastes_kb(callback_data.dop, callback_data.what, (await state.get_data())['cake_ins'][f'{callback_data.what}']), parse_mode='HTML')
    await callback.answer()


@router.callback_query(kb.Cake.filter(F.action == 'tastes'))
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



@router.callback_query(kb.Cake.filter(F.action == 'confirm_tastes'))
async def confirm_ingrs_taste(callback: CallbackQuery, callback_data: Cake, state: FSMContext):
    await callback.message.edit_text(text='Продолжайте выбор начинок соответствующих ингридиентов. По завершении нажмите кнопку \n"Опубликовать торт ✅".', reply_markup=kb.cake_ingrs_kb((await state.get_data())['cake_type'], (await state.get_data())['cake_ins']), parse_mode='HTML')
    await callback.answer()


@router.callback_query(kb.Cake.filter(F.action=='confirm_order'))
async def confirm_order(callback: CallbackQuery, callback_data: Cake, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    try:
        SyncORM.insert_conf_cake(callback.from_user.id, await state.get_data())
        await bot.edit_message_text(text=f'Поздравляем с созданием нового продукта!\n\nВыберите следующее действие кнопочками ниже)', chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=kb.createNew)
    except Exception as e:
        await bot.edit_message_text(text=f'Торт с такими ингридиентами невозможен. Попробуйте ещё раз. {data['approve_text']}', chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=kb.kb_for_approve())
    finally:
    	print('inserted')
    