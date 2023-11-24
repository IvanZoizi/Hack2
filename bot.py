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
    args = message.get_args()
    reference = decode_payload(args)
    if reference:
        await message.answer(f"Здравствуйте, для того чтобы оставить заявку на работу для начала ответьте на пару вопросов.\n"
                             f"Как Вас зовут?")
        await Reg.name.set()


@dp.message_handler(state=Reg.name)
async def reg_name_state(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отлично, теперь укажите ваш номер телефона")
    await Reg.phone.set()


@dp.message_handler(state=Reg.phone)
async def reg_phone_state(message: types.Message, state: FSMContext):
    keyboards = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboards.add([types.KeyboardButton(text='Полная занятость'), types.KeyboardButton(text='Частичная занятость')])
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
    await message.answer("", reply_markup=keyboards)
    await Reg.type_.set()


if __name__ == '__main__':
    db = Dbase(r'./src/db.sqlite3')
    #host.run()
    executor.start_polling(dp, skip_updates=True)
