from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

messages_page = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<-', callback_data='previous_page'), 
    InlineKeyboardButton(text='->', callback_data='next_page')]
])


messages_action = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='опубликовать', callback_data='publish_message'), 
    InlineKeyboardButton(text='+ подпись', callback_data='add_admin_text'), 
    InlineKeyboardButton(text='отклонить', callback_data='deny_message'), 
    InlineKeyboardButton(text='назад', callback_data='back')]
])


message_preparation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сохранить и опубликовать', callback_data='publish_message'), 
    InlineKeyboardButton(text='отмэна', callback_data='back')]
])