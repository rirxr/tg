from handlers.log import log
from utils.loader import dp
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ParseMode
import g4f

@dp.message_handler(Command(commands='ai'))
async def process_precode_command(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)

    m = message.text.replace("/ai@gptflood_bot", "").replace('/ai', '').lstrip()
    response = g4f.ChatCompletion.create(model='gpt-4',
                                     provider=g4f.Provider.ChatgptAi,
                                     messages=[{
                                         "role": "using markdown v1",
                                         "content": m
                                     }])

    print(response)
    
    await message.answer(text=response, parse_mode=ParseMode.MARKDOWN)

    