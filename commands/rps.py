from handlers.log import log
from utils.loader import dp, bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from random import choice

@dp.message_handler(commands=['rps'])
async def start_game_rps(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)

    await message.reply("Режим игры: С нейросетью",
                        reply_markup=get_keyboard())


def determine_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "draw"
    elif (user_choice == "камень" and bot_choice == "ножницы") or (
            user_choice == "ножницы"
            and bot_choice == "бумага") or (user_choice == "бумага"
                                            and bot_choice == "камень"):
        return "user"
    else:
        return "bot"


def get_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Камень", callback_data="rps камень"),
        InlineKeyboardButton("Ножницы", callback_data="rps ножницы"),
        InlineKeyboardButton("Бумага", callback_data="rps бумага"))
    return keyboard


@dp.callback_query_handler(lambda c: c.data.startswith('rps'))
async def handle_buttons(callback_query: CallbackQuery):
    user_choice = callback_query.data.replace("rps ", "").strip()
    bot_choice = choice(["камень", "ножницы", "бумага"])
    winner = determine_winner(user_choice, bot_choice)

    result_message = f"@{callback_query.from_user.username} выбрал(-а): {user_choice}\nНейросеть выбрала: {bot_choice}\n\n"

    if winner == "user":
        result_message += "Поздравляю, ты победил! 🎉"
    elif winner == "bot":
        result_message += "Нейросеть победила. Попробуй ещё раз! 👾"
    else:
        result_message += "Ничья. Попробуй ещё раз! 🤝"

    await bot.send_message(callback_query.message.chat.id,
                           text=result_message,
                           reply_markup=get_keyboard())
