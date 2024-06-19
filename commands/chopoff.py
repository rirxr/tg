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

@dp.message_handler(commands=['отрубить', 'chopoff'])
async def blowup(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)

    if message.text == "/отрубить" or message.text == "/chopoff" or message.text == "/chopoff@gptfloodbot":
        return await bot.send_message(message.chat.id,
                                      "Вы не указали участника.")

    msg = id(message.text)[1:]
    do = remove_words(message.text)

    if do == "":
        return await bot.send_message(message.chat.id,
                                      "И что отрубать будешь?\n\nИспользование: /отрубить [тег] [часть].")
    
    namefrom = link(message.from_user.full_name, f'https://t.me/{message.from_user.username}')
    nameto = link(msg, f'https://t.me/{msg}')

    string = f"🪓 | {namefrom} отрубил(-а) {nameto} {do}"

    if message.from_user.username == msg:
        string += "\n\nТы не способен(-на) регенерировать части тела.."

    await bot.send_message(message.chat.id, string, disable_web_page_preview=True)
