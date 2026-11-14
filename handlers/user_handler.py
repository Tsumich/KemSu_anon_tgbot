from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db import get_last_message, save_message

router = Router()

class SMS(StatesGroup):
    name = State()
    message = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Ку! Хочешь что то сказать? тогда пиши команду /sms')

@router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer('тут тебе никто не поможет друк, но ты можешь прислать смс командой /sms')

@router.message(Command('sms'))
async def sms_name(message: Message, state: FSMContext):
    await state.set_state(SMS.name)
    kb = [[types.KeyboardButton(text="Не хочу указывать имя", )]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    if await get_last_message(message.from_user.id) == False:
        print("с последнего смс менее 15 минут")
        await message.answer('Прости, друк, но смс не чаще чем раз в 15 минут!')
        return
    await message.answer('Как вы хотите представиться?', reply_markup=keyboard)


@router.message(SMS.name)
async def sms_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text) # типа сохранение имени после получения
    await state.set_state(SMS.message) # после получения данных меняем состояние
    await message.answer("Отлично! А теперь наберите ваше послание", reply_markup=types.ReplyKeyboardRemove())

@router.message(SMS.message)
async def sms_name(message: Message, state: FSMContext):
    await state.update_data(new_message=message.text)

    data = await state.get_data()

    author_name = data.get("name", "Анон")
    new_message_text = data.get("new_message")
    user_id = message.from_user.id

    if author_name == "Не хочу указывать имя":
        author_name = "Анон"

    await save_message(author_name, new_message_text, user_id)
    await message.answer("Отлично! Ваше сообщение сохранено! Ждите публикации ")

    await state.clear()

