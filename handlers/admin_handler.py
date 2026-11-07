from aiogram import Router, F
import os
from dotenv import load_dotenv
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from utils.messages_utils import get_content

from db import get_all_message, get_message, update_subtext
from keyboards import messages_page, messages_action, message_preparation

load_dotenv()
CHANEL_ID = os.getenv("CHANEL_ID")

OFFSET = 5

class Check_SMS(StatesGroup):
    start = State()
    open_sms = State()
    chng_subtext = State()
    deny_sms = State()

admin_router = Router()

@admin_router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer('234')

#----------------- ВЫВОД СООБЩЕНИЙ -------------------

@admin_router.message(Command('show'))
async def sms_name(message: Message, state: FSMContext):
    await state.update_data(offset=0)
    messages = await get_all_message(OFFSET, 0)
    if not messages:
        await message.answer("Список пуст")
        return
    
    content = get_content(messages)

    await message.answer(content, parse_mode="HTML", reply_markup=messages_page)
    await state.set_state(Check_SMS.open_sms)

#----------------- СЛЕДУЮЩАЯ СТРАНИЦА -------------------

@admin_router.callback_query(F.data == 'next_page')
async def next_page(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_offset = data.get("offset", 0)
    new_offset = current_offset + OFFSET

    messages = await get_all_message(OFFSET, new_offset)
    if not messages:
        await callback.answer("Это последняя страница", show_alert=True)
        return

    await callback.answer('')
    await state.update_data(offset=new_offset)

    content = get_content(messages)

    try:
        await callback.message.edit_text(content, parse_mode="HTML", reply_markup=messages_page)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise e


#----------------- ПРЕДЫДУЩАЯ СТРАНИЦА -------------------

@admin_router.callback_query(F.data == 'previous_page')
async def previous_page(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_offset = data.get("offset", 0)

    if current_offset <= 0:
        await callback.answer("Вы на самой первой странице", show_alert=True)
        return

    new_offset = current_offset - OFFSET
    messages = await get_all_message(OFFSET, new_offset)
    if not messages:
        await callback.answer("Предыдущих сообщений не найдено", show_alert=True)
        return

    await callback.answer('')
    await state.update_data(offset=new_offset)

    content = get_content(messages)

    try:
        await callback.message.edit_text(content, parse_mode="HTML", reply_markup=messages_page)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise e

#----------------- АДМИН ВЫБРАЛ НОМЕР ПОСЛАНИЯ -------------------

@admin_router.message(Check_SMS.open_sms)
async def sms_name(message: Message, state: FSMContext):
    content = await get_message(message.text)
    await state.update_data(msg_id=message.text)
    id, author, text = content 
    await state.update_data(author=author)
    await state.update_data(text=text)
    content = f'{id} - {author} : <code>{text}</code>\n'
    await message.answer(content, parse_mode="HTML", reply_markup=messages_action)

#----------------- АДМИН ВЫБИРАЕТ ПОДПИСЬ -------------------

@admin_router.callback_query(F.data == 'add_admin_text')
async def previous_page(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Check_SMS.chng_subtext)
    await callback.message.answer("Какую подпись хотите добавить?", parse_mode="HTML")

@admin_router.message(Check_SMS.chng_subtext)
async def sms_name(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(admin_text=message.text)
    author = data.get("author")
    text = data.get("text")
    content = message.text + '\n\n'
    content += f'{author} : <code>{text}</code>\n'
    await message.answer(content, parse_mode="HTML", reply_markup=message_preparation)

#----------------- АДМИН ВЫБИРАЕТ ПУБЛИКОВАТЬ -------------------

@admin_router.callback_query(F.data == 'publish_message')
async def previous_page(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Check_SMS.start)
    data = await state.get_data()

    admin_text = data.get("admin_text", "")
    author = data.get("author")
    text = data.get("text")
    content = f"{admin_text}\n\n" if admin_text else ""
    content += f'{author} : <code>{text}</code>\n'

    await update_subtext(data.get("id"), data.get("admin_text"))
    print(CHANEL_ID)
    await callback.bot.send_message(
        chat_id=CHANEL_ID, 
        text=content, 
        parse_mode="HTML"
    )
    await callback.message.edit_text("Запостил в подслушку!")

#----------------- АДМИН ВЫБИРАЕТ ОТКЛОНИТЬ -------------------



#----------------- АДМИН ВЫБИРАЕТ ОТМЕНУ -------------------