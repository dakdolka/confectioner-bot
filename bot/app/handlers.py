from aiogram import F, Router
from typing import Union, Dict, Any
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import Message, CallbackQuery, WebAppData
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import json
from DataBase import cursor, db


	

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

class Cake(StatesGroup):
	name = State()
	weight = State()
	filling = State()
	newType = State()
	newType2 = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
	userid = message.from_user.id
	print(userid)
	request = f"SELECT fuserid FROM tconditers WHERE fuserid LIKE {userid}"
	cursor.execute(request)
	matchids = cursor.fetchall()
	if matchids:
		request = f"SELECT fname FROM tconditers WHERE fuserid LIKE {userid}"
		cursor.execute(request)
		name = cursor.fetchall()[0][0]
		await message.answer(text=f'Здравствуйте, {name}! Хотите создать новый продукт?', reply_markup=kb.createNew)
	else:
		await message.answer('======Добро пожаловать!!=======\nЗаполните анкету', reply_markup=kb.start)


@router.message(Command("w"))
async def hello_start(message: Message):
	userid = message.from_user.id
	print(userid)
	await message.answer('jnjnjnjnjn', reply_markup=kb.webapp)


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
	await state.set_state(Reg.aboutCond)
	await message.answer(text='Расскажите о себе:', reply_markup=kb.skip1)
	await state.update_data(fexp=message.text)


@router.callback_query(F.data == 'skip1')
async def add_social1(callback: CallbackQuery, state: FSMContext):
	await state.update_data(fabout='')
	await callback.message.edit_text(text='Добавьте свои социальные сети', reply_markup=await kb.social())


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
	await callback.message.edit_text(text=f'Подтвердите данные профиля:\nИмя: {data.get("fname", "Не указано")} \nОпыт работы: {data.get("fexp", "Не указано")} \nО себе: {data.get("fabout", "Не указано")} \n\nСОЦСЕТИ\n\nYoutube: {data.get("fyoutube", "Не указано")} \nVK: {data.get("fvk", "Не указано")} \nInstagram: {data.get("finstagram", "Не указано")} \n',
									 reply_markup=kb.approve)


@router.callback_query(F.data == 'changeProfile')
async def choose_change(callback: CallbackQuery):
	await callback.answer()
	await callback.message.answer(text='Что вы хотели бы исправить?', reply_markup=await kb.changeProfileKb())


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
	await message.answer(text=f'Подтвердите данные профиля:\nИмя: {data.get("fname", "Не указано")} \nОпыт работы: {data.get("fexp", "Не указано")} \nО себе: {data.get("fabout", "Не указано")} \n\nСОЦСЕТИ\n\nYoutube: {data.get("fyoutube", "Не указано")} \nVK: {data.get("fvk", "Не указано")} \nInstagram: {data.get("finstagram", "Не указано")} \n',
									 reply_markup=kb.approve)


@router.message(Reg.changeExp)
async def changeName(message: Message, state: FSMContext):
	await state.update_data(fexp=message.text)
	data = dict(await state.get_data())
	await message.answer(text=f'Подтвердите данные профиля:\nИмя: {data.get("fname", "Не указано")} \nОпыт работы: {data.get("fexp", "Не указано")} \nО себе: {data.get("fabout", "Не указано")} \n\nСОЦСЕТИ\n\nYoutube: {data.get("fyoutube", "Не указано")} \nVK: {data.get("fvk", "Не указано")} \nInstagram: {data.get("finstagram", "Не указано")} \n',
									 reply_markup=kb.approve)


@router.message(Reg.changeAbout)
async def changeName(message: Message, state: FSMContext):
	await state.update_data(fabout=message.text)
	data = dict(await state.get_data())
	await message.answer(text=f'Подтвердите данные профиля:\nИмя: {data.get("fname", "Не указано")} \nОпыт работы: {data.get("fexp", "Не указано")} \nО себе: {data.get("fabout", "Не указано")} \n\nСОЦСЕТИ\n\nYoutube: {data.get("fyoutube", "Не указано")} \nVK: {data.get("fvk", "Не указано")} \nInstagram: {data.get("finstagram", "Не указано")} \n',
									 reply_markup=kb.approve)


@router.callback_query(F.data == 'end_reg')
async def end_reg(callback: CallbackQuery, state: FSMContext):
	regData = dict(await state.get_data())
	await state.clear()

	yt = regData.get('fyoutube', '')
	vk = regData.get('fvk', '')
	inst = regData.get('finstagram', '')
	request = f"INSERT INTO tconditers (fuserId, fname, fexp, fabout, fyoutube, fvk, finstagram) VALUES {tuple([callback.from_user.id] + list(regData.values())[:3] + [yt, vk, inst])}"
	print(request)
	cursor.execute(request)
	db.commit()

	await callback.message.edit_text(text='Регистрация успешно завершена! Хотите создать свой первый продукт?',
						 reply_markup=kb.createNew)


@router.callback_query(F.data == 'CreateNew')  # Выбор торт или что-то другое
async def create(callback: CallbackQuery):
	await callback.message.answer(text='Какое творение вы хотите создать?', reply_markup=kb.cakeOrNot)
	await callback.answer()


@router.callback_query(F.data == 'Cake')  # Выбор типа торта
async def createCake1(callback: CallbackQuery):
	request = f'SELECT fproductid FROM tproducttype'
	cursor.execute(request)
	fproductid = max(list(map(lambda x: x[0], cursor.fetchall())) or [-1]) + 1

	request = f'INSERT INTO tproductType (fcreator, ftypeName, fproductid) VALUES ({callback.from_user.id}, "cake", {fproductid})'
	cursor.execute(request)
	db.commit()

	request = f"SELECT fcaketypes FROM tcaketypes"
	cursor.execute(request)
	cakeTypes = list(map(lambda x: x[0], cursor.fetchall()))
	print(cakeTypes)

	await callback.answer()
	await callback.message.edit_text(text='Какого вида будет ваш торт?', reply_markup=await kb.createInlineCake(cakeTypes, fproductid))


@router.callback_query(kb.CakeTypesCb.filter())
async def add_social_link(callback: CallbackQuery, callback_data: kb.CakeTypesCb):
	await callback.answer()
	request = f'INSERT INTO ttort (fproductId, ftypename) VALUES ({callback_data.productId}, "{callback_data.cakeType}")'
	cursor.execute(request)
	db.commit()

	request = f'SELECT fcakecomponents FROM tcakecomponents WHERE ftypename LIKE "{callback_data.cakeType}"'
	cursor.execute(request)
	components = dict(map(lambda x: (x.split(',')[0], x.split(',')[1]), list(cursor.fetchall())[0][0].split(';')))
	print(components)
	await callback.message.edit_text(text='Выберить компоненты торта', reply_markup=await kb.cakeComponents(components))


@router.callback_query(kb.ChooseComponentCb.filter())
async def choose_component(callback: CallbackQuery, callback_data: kb.ChooseComponentCb):
	await callback.answer()
	request = f'SELECT fname FROM {callback_data.componentTable}'
	cursor.execute(request)
	componentTypes = list(map(lambda x: x[0], cursor.fetchall()))
	print(componentTypes)
	await callback.message.edit_text(text=f'Выберите компонент {callback_data.componentName} для вашего торта', reply_markup=await kb.cakeComponentTypes(componentTypes))









