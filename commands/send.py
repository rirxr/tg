from handlers.log import log
from utils.admins import admin
from utils.loader import dp, bot
from aiogram.types import Message
import os

@dp.message_handler(commands=['send'])
async def send(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)

    msg = message.text.split()
    msg = ' '.join(msg[1:])

    if len(msg) <= 1:
        return await message.answer("Вы не указали сообщение.")
    
    if not admin(message.from_user.id):
        return await message.reply("У Вас нет прав на эту команду.")

    for file in os.listdir('./users'):
        file = file.replace('.json', '')

        try:
            await bot.send_message(chat_id=file, text=msg)
        except:
            pass

