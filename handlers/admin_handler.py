from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

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
    await callback.answer('') # чтобы при нажатии на инлайн кнопку она не подсвечивалась
    await callback.message.edit_text("Вперед ", reply_markup= messages_page) # edit!! чтобы сообщение не отправлялось новое
    new_offset = await state.get_data()
    new_offset = new_offset["offset"] + 2
    await state.update_data(offset=new_offset)
    messages = await get_all_message(new_offset)
    if not messages:
        await callback.message.answer("Список пуст")
        return
    
    content = 'Вот все неопубликованные сообщения:\n\n'
    for id, author, text in messages:
        content += f'{id} - {author} : <code>{text}</code>\n'
    content += "\n Укажите id сообщения с которыми хотите взаимодействовать"

    await callback.message.edit_text(content, parse_mode="HTML", reply_markup=messages_page)


@admin_router.callback_query(F.data == 'previous_page')
async def next_page(callback: CallbackQuery, state: FSMContext):
    await callback.answer('') # чтобы при нажатии на инлайн кнопку она не подсвечивалась
    await callback.message.edit_text("Назад", reply_markup= messages_page) 
    new_offset = await state.get_data()
    new_offset = new_offset["offset"] - 2
    await state.update_data(offset=new_offset)
    messages = await get_all_message(new_offset)
    if not messages:
        await callback.message.answer("Список пуст")
        return
    
    content = 'Вот все неопубликованные сообщения:\n\n'
    for id, author, text in messages:
        content += f'{id} - {author} : <code>{text}</code>\n'
    content += "\n Укажите id сообщения с которыми хотите взаимодействовать"

    await callback.message.edit_text(content, parse_mode="HTML", reply_markup=messages_page)


