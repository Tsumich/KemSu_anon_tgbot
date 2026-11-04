from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

messages_page = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<-', callback_data='previous_page'), 
    InlineKeyboardButton(text='->', callback_data='next_page')]
])

