from handlers.log import log
from utils.loader import dp, bot
from aiogram.types import Message
from aiogram.utils.markdown import link

def id(string):
    words = string.split()
    without_words = ' '.join(words[1:])

    return without_words

@dp.message_handler(commands=['связать', 'tie'])
async def blowup(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)
    
    if not message.reply_to_message:
        return await bot.send_message(message.chat.id,
                                      "Вы не указали участника. Для этого достаточно переслать сообщение.")
    
    msg = message.reply_to_message.from_user

    namefrom = link(message.from_user.full_name, f'https://t.me/{message.from_user.username}')
    nameto = link(msg.full_name, f'https://t.me/{msg.username}')

    string = f"🧶 | {namefrom} связал(-а) {nameto}"

    if message.from_user.username == msg:
        string += "\n\nКак тебе это удалось?"

    await bot.send_message(message.chat.id, string, disable_web_page_preview=True)
