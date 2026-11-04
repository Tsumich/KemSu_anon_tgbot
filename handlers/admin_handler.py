from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from db import get_all_message
from keyboards import messages_page


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
    await state.update_data(offset=0)
    messages = await get_all_message(0)
    if not messages:
        await message.answer("Список пуст")
        return
    
    content = 'Вот все неопубликованные сообщения:\n\n'
    for id, author, text in messages:
        content += f'{id} - {author} : <code>{text}</code>\n'
    content += "\n Укажите id сообщения с которыми хотите взаимодействовать"

    await message.answer(content, parse_mode="HTML", reply_markup=messages_page)

@admin_router.callback_query(F.data == 'next_page')
async def next_page(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_offset = data.get("offset", 0)
    new_offset = current_offset + 2

    messages = await get_all_message(new_offset)
    if not messages:
        await callback.answer("Это последняя страница", show_alert=True)
        return

    await callback.answer('')
    await state.update_data(offset=new_offset)

    content = 'Вот все неопубликованные сообщения:\n\n'
    for id, author, text in messages:
        content += f'{id} - {author} : <code>{text}</code>\n'
    content += "\n Укажите id сообщения с которыми хотите взаимодействовать"

    try:
        await callback.message.edit_text(content, parse_mode="HTML", reply_markup=messages_page)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise e


@admin_router.callback_query(F.data == 'previous_page')
async def previous_page(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_offset = data.get("offset", 0)

    if current_offset <= 0:
        await callback.answer("Вы на самой первой странице", show_alert=True)
        return

    new_offset = current_offset - 2
    messages = await get_all_message(new_offset)
    if not messages:
        await callback.answer("Предыдущих сообщений не найдено", show_alert=True)
        return

    await callback.answer('')
    await state.update_data(offset=new_offset)

    content = 'Вот все неопубликованные сообщения:\n\n'
    for id, author, text in messages:
        content += f'{id} - {author} : <code>{text}</code>\n'
    content += "\n Укажите id сообщения с которыми хотите взаимодействовать"

    try:
        await callback.message.edit_text(content, parse_mode="HTML", reply_markup=messages_page)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise e


