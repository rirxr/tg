from handlers.log import log
from utils.cjson import load, dump
from utils.loader import dp
from aiogram.types import Message

@dp.message_handler(commands=['reg', 'рег'])
async def reg(message: Message):
    await log(message)

    msg = message.text.split()

    if len(msg) <= 2:
        return await message.answer('Использование: /reg <фамилия> <имя>')
    
    data = load(message.from_user.id)
    data['name'] = msg[2]
    data['lastname'] = msg[1]
    dump(data)

    await message.answer(f'Регистрация завершена.\nОтныне Вы: {msg[1]} {msg[2]}\n\nТеперь Вам доступны все функции бота.')
    