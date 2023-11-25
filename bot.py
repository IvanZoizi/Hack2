import asyncio

import aioschedule as aioschedule
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile, ContentType
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram import types

import config
from func import Dbase

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


callback_data_courier = CallbackData('func', 'id_courier', 'id_order')
callback_data_done = CallbackData('ac', 'id_order')


class Reg(StatesGroup):
    name = State()
    phone = State()
    type_ = State()
    description = State()


class Menu(StatesGroup):
    get_menu = State()
    start = State()
    feedback_des = State()
    stars = State()


class Business(StatesGroup):
    get_menu = State()
    start = State()
    feedback_des = State()
    stars = State()


@dp.message_handler(commands=["start"])
async def handler(message: types.Message):
    await asyncio.create_task(db.new_user(message.from_user.id))
    args = message.get_args()
    reference = decode_payload(args)
    if reference:
        await message.answer(f"Здравствуйте, для того чтобы оставить заявку на работу для начала ответьте на пару вопросов.\n"
                             f"Как Вас зовут?")
        await Reg.name.set()
    else:
        ids = [i[0] for i in await asyncio.create_task(db.get_all())]
        ids_c = [i[0] for i in await asyncio.create_task(db.get_expectation_all())]
        if message.from_user.id in ids:
            await message.answer("Здравствуйте, тут Вы сможете получать информацию о доступных заказах")
        elif message.from_user.id in ids_c:
            await message.answer("Здравствуйте, Ваша заявка находится на модерации")
        else:
            keyboards = types.ReplyKeyboardMarkup()
            keyboards.add(types.KeyboardButton(text='Узнать меню'))
            keyboards.add(types.KeyboardButton(text='Узнать бизнес Ланчи'))
            await message.answer("Здравствуйте, тут Вы сможете узнать последние новости, "
                                 "зарегистрироваться на мероприятия от кухни", reply_markup=keyboards)


@dp.message_handler(state=Reg.name)
async def reg_name_state(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отлично, теперь укажите ваш номер телефона")
    await Reg.phone.set()


@dp.message_handler(state=Reg.phone)
async def reg_phone_state(message: types.Message, state: FSMContext):
    keyboards = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboards.add(types.KeyboardButton(text='Полная занятость'))
    keyboards.add(types.KeyboardButton(text='Частичная занятость'))
    await state.update_data(phone=message.text)
    await message.answer("Теперь нужно указать ваш тип занятости", reply_markup=keyboards)
    await Reg.type_.set()


@dp.message_handler(state=Reg.type_)
async def reg_type_state(message: types.Message, state: FSMContext):
    if message.text.capitalize() not in ['Полная занятость', 'Частичная занятость']:
        await message.answer("Я вас не понял, попробуйте еще раз")
        return
    keyboards = types.ReplyKeyboardRemove()
    await state.update_data(type=message.text)
    await message.answer("Расскажите о себе", reply_markup=keyboards)
    await Reg.description.set()


@dp.message_handler(state=Reg.description)
async def reg_description_state(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Вы успешно ответили на наши вопросы")
    data = await state.get_data()
    await asyncio.create_task(db.new_courier(message.from_user.id, message.from_user.username, data))
    await state.finish()


async def get_menu_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup()
    for i in ['Первое блюдо', 'Второе блюдо', 'Салат', 'Десерт', 'Напиток']:
        keyboard.add(types.KeyboardButton(i))
    await message.answer('Какой вид блюда Вы бы хотели увидеть?', reply_markup=keyboard)
    await Menu.get_menu.set()


@dp.message_handler(state=Menu.get_menu)
async def get_menu_start_(message: types.Message, state: FSMContext):
    if message.text not in ['Первое блюдо', 'Второе блюдо', 'Салат', 'Десерт', 'Напиток']:
        await message.answer("Попробуйте еще раз")
        return
    food = await asyncio.create_task(db.get_food_type(message.text))
    start_num = 0
    keyboard = types.ReplyKeyboardMarkup()
    if len(food) - start_num != 1:
        for i in ['Далее', 'Оставить отзыв', 'Назад']:
            keyboard.add(types.KeyboardButton(i))
    else:
        keyboard.add(types.KeyboardButton('Оставить отзыв'))
        keyboard.add(types.KeyboardButton('Назад'))  # https://t.me/botusername?feedback=242915
    photo = InputFile('./src/media/' + food[start_num][9])
    await state.update_data(ref=food[start_num][0], start_num=start_num + 1, get=message.text)
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=f"<code>{food[start_num][1]}</code>\n"
                                                                            f"Цена - {food[start_num][2]}\n"
                                                                            f"Состав блюда - {food[start_num][3]}\n", reply_markup=keyboard, parse_mode='html')
    await Menu.start.set()


@dp.message_handler(state=Menu.start)
async def start_menu(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        keyboards = types.ReplyKeyboardMarkup()
        keyboards.add(types.KeyboardButton(text='Узнать меню'))
        keyboards.add(types.KeyboardButton(text='Оставить отзыв на продукцию'))
        await message.answer("Вы вернулись в главное меню", reply_markup=keyboards)
        return
    if message.text == 'Оставить отзыв':
        return await asyncio.create_task(feedback(message, state))
    data = await state.get_data()
    food = await asyncio.create_task(db.get_food_type(data['get']))
    start_num = data['start_num']
    keyboard = types.ReplyKeyboardMarkup()
    if len(food) - start_num != 1:
        for i in ['Далее', 'Оставить отзыв', 'Назад']:
            keyboard.add(types.KeyboardButton(i))
    else:
        keyboard.add(types.KeyboardButton('Оставить отзыв'))
        keyboard.add(types.KeyboardButton('Назад'))
    photo = InputFile('./src/media/' + food[start_num][9])
    await state.update_data(ref=food[start_num][0], start_num=start_num + 1)
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=f"<code>{food[start_num][1]}</code>\n"
                                                                            f"Цена - {food[start_num][2]}\n"
                                                                            f"Состав блюда - {food[start_num][3]}\n", reply_markup=keyboard, parse_mode='html')


@dp.message_handler(commands='feedback', state=Menu.start)
async def feedback(message: types.Message, state: FSMContext):
    await message.answer("Расскажите что вы думаете о нашем товаре")
    await Menu.feedback_des.set()


@dp.message_handler(state=Menu.feedback_des)
async def feedback_des(message: types.Message, state: FSMContext):

    await state.update_data(des=message.text)
    keyboard = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
    for i in ['1/2/3/4/5'.split('/')]:
        keyboard.add(types.KeyboardButton(text=i[0].capitalize()), types.KeyboardButton(text=i[1].capitalize()), types.KeyboardButton(text=i[2].capitalize()), types.KeyboardButton(text=i[3].capitalize()), types.KeyboardButton(text=i[4].capitalize()))
    await message.answer("Поставьте оценку нашей продукции", reply_markup=keyboard)
    await Menu.stars.set()


@dp.message_handler(state=Menu.stars)
async def stars(message: types.Message, state: FSMContext):
    if message.text not in ['1', '2', '3', '4', '5']:
        return await message.answer("Попробуйте еще раз")
    await state.update_data(stars=message.text)
    data = await state.get_data()
    await state.finish()
    await asyncio.create_task(db.new_feedback(message.from_user.username, data))
    keyboards = types.ReplyKeyboardMarkup()
    keyboards.add(types.KeyboardButton(text='Узнать меню'))
    keyboards.add(types.KeyboardButton(text='Оставить отзыв на продукцию'))
    await message.answer("Спасибо за ваше мнение!", reply_markup=keyboards)


async def get_bisness_start_(message: types.Message, state: FSMContext):
    food = await asyncio.create_task(db.get_business())
    start_num = 0
    keyboard = types.ReplyKeyboardMarkup()
    if len(food) - start_num != 1:
        for i in ['Далее', 'Оставить отзыв', 'Назад']:
            keyboard.add(types.KeyboardButton(i))
    else:
        keyboard.add(types.KeyboardButton('Оставить отзыв'))
        keyboard.add(types.KeyboardButton('Назад'))  # https://t.me/botusername?feedback=242915
    photo = InputFile('./src/media/' + food[start_num][9])
    await state.update_data(ref=food[start_num][0], start_num=start_num + 1)
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=f"<code>{food[start_num][1]}</code>\n"
                                                                            f"Цена - {food[start_num][2]}\n"
                                                                            f"Состав блюда - {food[start_num][8]}\n", reply_markup=keyboard, parse_mode='html')
    await Business.start.set()


@dp.message_handler(state=Business.start)
async def start_bisness(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        keyboards = types.ReplyKeyboardMarkup()
        keyboards.add(types.KeyboardButton(text='Узнать меню'))
        keyboards.add(types.KeyboardButton(text='Узнать бизнес Ланчи'))
        await message.answer("Вы вернулись в главное меню", reply_markup=keyboards)
        return
    if message.text == 'Оставить отзыв':
        return await asyncio.create_task(feedback_bisness(message, state))
    data = await state.get_data()
    food = await asyncio.create_task(db.get_business())
    start_num = data['start_num']
    keyboard = types.ReplyKeyboardMarkup()
    if len(food) - start_num != 1:
        for i in ['Далее', 'Оставить отзыв', 'Назад']:
            keyboard.add(types.KeyboardButton(i))
    else:
        keyboard.add(types.KeyboardButton('Оставить отзыв'))
        keyboard.add(types.KeyboardButton('Назад'))
    photo = InputFile('./src/media/' + food[start_num][9])
    await state.update_data(ref=food[start_num][0], start_num=start_num + 1)
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=f"<code>{food[start_num][1]}</code>\n"
                                                                            f"Цена - {food[start_num][2]}\n"
                                                                            f"Состав блюда - {food[start_num][8]}\n", reply_markup=keyboard, parse_mode='html')


@dp.message_handler(commands='feedback', state=Business.start)
async def feedback_bisness(message: types.Message, state: FSMContext):
    await message.answer("Расскажите что вы думаете о нашем товаре")
    await Business.feedback_des.set()


@dp.message_handler(state=Business.feedback_des)
async def feedback_de_bisness(message: types.Message, state: FSMContext):

    await state.update_data(des=message.text)
    keyboard = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
    for i in ['1/2/3/4/5'.split('/')]:
        keyboard.add(types.KeyboardButton(text=i[0].capitalize()), types.KeyboardButton(text=i[1].capitalize()), types.KeyboardButton(text=i[2].capitalize()), types.KeyboardButton(text=i[3].capitalize()), types.KeyboardButton(text=i[4].capitalize()))
    await message.answer("Поставьте оценку нашей продукции", reply_markup=keyboard)
    await Business.stars.set()


@dp.message_handler(state=Business.stars)
async def stars_bisness(message: types.Message, state: FSMContext):
    if message.text not in ['1', '2', '3', '4', '5']:
        return await message.answer("Попробуйте еще раз")
    await state.update_data(stars=message.text)
    data = await state.get_data()
    await state.finish()
    await asyncio.create_task(db.new_feedback_business(message.from_user.username, data))
    keyboards = types.ReplyKeyboardMarkup()
    keyboards.add(types.KeyboardButton(text='Узнать меню'))
    keyboards.add(types.KeyboardButton(text='Узнать бизнес Ланчи'))
    await message.answer("Спасибо за ваше мнение!", reply_markup=keyboards)


@dp.message_handler()
async def get_text(message: types.Message, state: FSMContext):
    if message.text == 'Узнать меню':
        await asyncio.create_task(get_menu_start(message, state))
    elif message.text == 'Узнать бизнес Ланчи':
        await asyncio.create_task(get_bisness_start_(message, state))


async def new_courier():
    all_courier = await asyncio.create_task(db.get_expectation_all())
    for elem in all_courier:
        courier = await asyncio.create_task(db.get_courier(elem[0]))
        if courier:
            await bot.send_message(chat_id=courier[0], text='Поздравляем вас, вы теперь официально стали курьером!')
            await asyncio.create_task(db.delete(courier[0]))


async def new_order():
    order = await asyncio.create_task(db.get_order())
    print(order)
    if order:
        courier = await asyncio.create_task(db.get_all())
        for elem in courier:
            send_get = await asyncio.create_task(db.get_send(elem[0], order[4]))
            if not send_get:
                print(order[4])
                print(order[2])
                print(order[3])
                print(order[6])
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Взять заказ', callback_data=callback_data_courier.new(id_courier=elem[0], id_order=order[4])))
                await bot.send_message(chat_id=elem[0], text=f'Заказ № {order[4]}\n'
                                                             f'Получатель - {order[2]}. Номер телефона - {order[3]}\n'
                                                             f'Этаж - {order[6]}', reply_markup=keyboard)
                await asyncio.create_task(db.send(elem[0], order[4]))
                await asyncio.create_task(db.delete(elem[0]))


@dp.callback_query_handler(callback_data_courier.filter())
async def call_back_def(call: types.CallbackQuery, data: dict):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Заказ выполнен',
                                            callback_data=callback_data_done.new(id_order=data['id_order'])))
    courier = await asyncio.create_task(db.get_courier(data['id_courier']))
    await asyncio.create_task(db.new_delivery(data['id_order'], courier[2], courier[3]))
    await call.message.edit_text("Вы успешно взяли заказ", reply_markup=keyboard)


async def scheduler():
    try:
        aioschedule.every().minute.do(new_courier)
        aioschedule.every().second.do(new_order)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
    except Exception as ex:
        pass


async def on_startup(dp):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    db = Dbase(r'./src/db.sqlite3')
    #host.run()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
