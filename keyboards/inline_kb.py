from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_delete_news_keyboard(date):
    kb = InlineKeyboardMarkup()
    btn_delete = InlineKeyboardButton('Удалить новость', callback_data=f'news {date}')
    kb.add(btn_delete)
    return kb
