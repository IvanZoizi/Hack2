import asyncio

import aioschedule as aioschedule
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile, ContentType
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram import types

import config
from func import Dbase

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Reg(StatesGroup):
    name = State()
    phone = State()
    type_ = State()
    description = State()


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
            await message.answer("Здравствуйте, тут Вы сможете узнать последние новости, "
                                 "зарегистрироваться на мероприятия от кухни")


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


async def new_courier():
    all_courier = await asyncio.create_task(db.get_expectation_all())
    for elem in all_courier:
        courier = await asyncio.create_task(db.get_courier(elem[0]))
        if courier:
            await bot.send_message(chat_id=courier[0], text='Поздравляем вас, вы теперь официально стали курьером!')
            await asyncio.create_task(db.delete(courier[0]))


async def scheduler():
    try:
        aioschedule.every().seconds.do(new_courier)
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
