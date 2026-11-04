from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db import get_all_message

class Check_SMS(StatesGroup):
    show_sms = State()
    open_sms = State()
    send_sms = State()
    deny_sms = State()

admin_router = Router()

@admin_router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer('234')


@admin_router.message(Command('show'))
async def sms_name(message: Message, state: FSMContext):
    await state.set_state(Check_SMS.show_sms)
    messages = await get_all_message()
    if not messages:
        await message.answer("Список пуст")
        return
    
    content = 'Вот все неопубликованные сообщения:\n\n'
    for id, author, text in messages:
        content += f'{id} - {author} : <code>{text}</code>\n'
    content += "\n Укажите id сообщения с которыми хотите взаимодействовать"
    await message.answer(content, parse_mode="HTML")
    