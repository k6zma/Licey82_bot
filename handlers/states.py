from aiogram.dispatcher.filters.state import State, StatesGroup


class NewsStates(StatesGroup):
    title = State()
    content = State()
    image = State()


class CreateGroupStates(StatesGroup):
    group_name = State()


class DeleteGroupStates(StatesGroup):
    group_name = State()


class StartStates(StatesGroup):
    group_name = State()


class SelectGroupStates(StatesGroup):
    group_name = State()


class ScheduleStates(StatesGroup):
    select_group = State()
    image = State()


class DeleteScheduleStates(StatesGroup):
    select_group = State()
