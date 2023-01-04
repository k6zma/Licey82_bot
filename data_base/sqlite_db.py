import sqlite3
from datetime import datetime
from sqlite3 import IntegrityError
from create_bot import bot

base = sqlite3.connect('licey82.db')
cursor = base.cursor()


def sql_start():
    if base:
        print('База данных подключена!')
    cursor.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name_group TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS news (dt DATETIME, title TEXT, content TEXT, img TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS groups (name TEXT PRIMARY KEY, schedule TEXT)')
    base.commit()


async def get_group(name):
    return [i for i in cursor.execute('SELECT * FROM groups WHERE name = ?', (name,))]


async def get_only_such_users(name):
    return [i for i in cursor.execute('SELECT * FROM users WHERE name_group = ?', (name,))]


async def create_schedule(state):
    data = await get_data_from_proxy(state)
    cursor.execute('UPDATE groups SET schedule = ? WHERE name = ?',
                   (data['image'], data['group']))
    base.commit()


async def delete_schedule(name):
    cursor.execute('UPDATE groups SET schedule = ? WHERE name = ?', (None, name))
    base.commit()


async def add_user(user_id):
    cursor.execute('INSERT INTO users VALUES (?, ?)', (user_id, 'no_group'))
    base.commit()


async def get_data_from_proxy(state):
    async with state.proxy() as data:
        return data


async def add_news(state):
    proxy_data = await get_data_from_proxy(state)
    cursor.execute('INSERT INTO news VALUES (?, ?, ?, ?)', (datetime.now(),) + tuple(proxy_data.values()))
    base.commit()


async def get_news():
    return [n for n in cursor.execute('SELECT * FROM news')]


async def delete_news(date):
    datetime_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    cursor.execute('DELETE FROM news WHERE dt = ?', (datetime_obj,))
    base.commit()


async def get_all_groups():
    return [_ for _ in cursor.execute('SELECT * FROM groups')]


async def delete_group(name):
    cursor.execute('DELETE FROM groups WHERE name = ?', (name,))
    base.commit()


async def add_group(name, msg):
    try:
        cursor.execute('INSERT INTO groups VALUES (?, ?)', (name, None))
        base.commit()
    except IntegrityError:
        bot.send_message(msg.chat.id, 'Данный класс уже создан!')


async def get_all_users():
    return [u for u in cursor.execute('SELECT * FROM users')]


async def change_user_group(user_id, group_name):
    cursor.execute('UPDATE users SET name_group = ? WHERE tg_id = ?', (group_name, user_id))
    base.commit()


