from handlers.log import log
from utils.loader import dp, bot
from aiogram.types import Message
from aiogram.utils.markdown import link

def remove_words(string):
    words = string.split()
    without_words = ' '.join(words[2:])

    return without_words

def id(string):
    words = string.split()
    without_words = ' '.join(words[1::3])

    return without_words

@dp.message_handler(commands=['заставить', 'force'])
async def blowup(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)

    if message.text == "/заставить" or message.text == "/force" or message.text == "/force@gptfloodbot":
        return await bot.send_message(message.chat.id,
                                      "Вы не указали участника.")

    msg = id(message.text)[1:]
    do = remove_words(message.text)

    if do == "":
        return await bot.send_message(message.chat.id,
                                      "И что он(-а) делать будет?\n\nИспользование: /заставить [тег] [действие].")
    
    namefrom = link(message.from_user.full_name, f'https://t.me/{message.from_user.username}')
    nameto = link(msg, f'https://t.me/{msg}')

    string = f"🔥 | {namefrom} заставил(-а) {nameto} {do}"

    if message.from_user.username == msg:
        string += "\n\nПереборол лень?"

    await bot.send_message(message.chat.id, string, disable_web_page_preview=True)
