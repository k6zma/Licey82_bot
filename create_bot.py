from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


storage = MemoryStorage()

bot = Bot(token='5797613512:AAEA_X53UFFWyg6qfnWBhQtWS0rHJwovEmU')

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
