from create_bot import bot


async def delete_inline_keyboard(message):
    await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=message.message_id,
                                        reply_markup=None)
