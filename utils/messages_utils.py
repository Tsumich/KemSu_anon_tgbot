def get_content(messages):
    content = 'Вот все неопубликованные сообщения:\n\n'
    for id, author, text in messages:
        short_text = text[:30]
        content += f'{id} - {author} : <code>{short_text}</code>\n'
    content += "\n Укажите id сообщения с которыми хотите взаимодействовать"
    return content