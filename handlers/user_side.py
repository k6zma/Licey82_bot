from aiogram import types
from create_bot import bot, dp
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from handlers import states
from keyboards import usually_kb


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    all_users_id = [id_[0] for id_ in await sqlite_db.get_all_users()]
    if message.from_user.id not in all_users_id:
        await sqlite_db.add_user(message.from_user.id)

    await bot.send_message(message.chat.id, 'Здарова! Я бот Лицея №82. Помощь по командам /help')
    await bot.send_message(message.chat.id, 'Выбери класс в котором учишься, либо напиши любой текст,'
                                            'чтобы пропустить это',
                           reply_markup=usually_kb.group_keyboard(await sqlite_db.get_all_groups()))
    await states.StartStates.group_name.set()


@dp.message_handler(state=states.StartStates.group_name)
async def start_state(message: types.Message, state: FSMContext):
    all_group_names = [_[0] for _ in await sqlite_db.get_all_groups()]
    if message.text in all_group_names:
        await sqlite_db.change_user_group(message.from_user.id, message.text)
        await bot.send_message(message.chat.id, f'Окей, я прикрепил тебя к классу {message.text}',
                               reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, 'Ты пропустил выбор класса, но ты всегда сможешь'
                                                ' выбрать его с помощью /select_group',
                               reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Так, вижу ты не знаешь команды, ну ничего страшного, держи список этих комманд: \n • /start - начало работы с ботом  \n • /select_group - выбор класса \n • /delete_me_from_group - этой командой вы можете удалить себя из текущей группы \n • /news - узнайте самые свежие новости нашего Лицея")


@dp.message_handler(commands=['select_group'])
async def select_group_command(message: types.Message):
    all_groups = await sqlite_db.get_all_groups()
    group_kb = usually_kb.group_keyboard(all_groups)
    await message.reply('Выбери класс', reply=False,
                        reply_markup=group_kb)
    await states.SelectGroupStates.group_name.set()


@dp.message_handler(state=states.SelectGroupStates.group_name)
async def select_group_state(message: types.Message, state: FSMContext):
    all_group_names = [_[0] for _ in await sqlite_db.get_all_groups()]
    if message.text in all_group_names:
        await sqlite_db.change_user_group(message.from_user.id, message.text)
        await bot.send_message(message.chat.id, f'Класс изменён',
                               reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, 'Класс который ты выбрал, не существует',
                               reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=['delete_me_from_group'])
async def delete_from_group(message: types.Message):
    await sqlite_db.change_user_group(message.from_user.id, None)
    await message.reply('Класс успешно отвязан', reply=False)


@dp.message_handler(commands=['news', 'новости'])
async def news_command(message: types.Message):
    news = await sqlite_db.get_news()
    for i in news[:3]:
        await bot.send_photo(message.chat.id, i[3], f'*{i[1]}*\n\n{i[2]}',
                             parse_mode='Markdown')
