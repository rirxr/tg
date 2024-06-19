from handlers.log import log
from utils.loader import dp
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.types import Message

@dp.message_handler(CommandStart())
async def process_start_command(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)

    await message.answer(text='''/ai - задать вопрос нейросети.
                                /rps - начать игру в КНБ.
                                /xo - начать игру в крестики-нолики.
                                /xoo - начать игру в крестики-нолики с кем-то.
                         
                                *** РП команды ***
                                /взорвать''')


@dp.message_handler(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='''/ai - задать вопрос нейросети.
                                /rps - начать игру в КНБ.
                                /xo - начать игру в крестики-нолики.
                                /xoo - начать игру в крестики-нолики с кем-то.
                         
                                *** РП команды ***
                                /взорвать''')

