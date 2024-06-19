from handlers.log import log
from utils.loader import dp, bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from random import randint

board = [[" " for _ in range(3)] for _ in range(3)]

def reset_board():
    global board
    board = [[" " for _ in range(3)] for _ in range(3)]

@dp.message_handler(commands=['xo'])
async def start_game_xo(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)

    keyboard = InlineKeyboardMarkup(row_width=3)
    for row in range(3):
        for col in range(3):
            button_text = board[row][col] if board[row][col] != " " else "-"
            callback_data = f"move {row} {col}"
            keyboard.insert(
                InlineKeyboardButton(button_text,
                                            callback_data=callback_data))

    keyboard.add(
        InlineKeyboardButton("Играть снова", callback_data="reset"))

    await message.answer("          <b>Крестики-нолики\nРежим игры: С нейросетью</b>",
                            reply_markup=keyboard)
    
@dp.callback_query_handler(lambda c: c.data.startswith('move'))
async def make_move(callback_query: CallbackQuery):
    row, col = map(int, callback_query.data.split()[1:])

    if board[row][col] != " ":
        await callback_query.answer("Эта клетка уже занята.",
                                    show_alert=True)
        return

    board[row][col] = "X"

    if check_winner_neuro(board, "X"):
        await callback_query.answer("Вы выиграли! Поздравляю!")
        board[row][col] = "X"
        await update_keyboard(callback_query.message)
        return

    if check_draw(board):
        await callback_query.answer("Ничья!")
        return

    computer_row, computer_col = make_computer_move(board)
    board[computer_row][computer_col] = "O"

    if check_winner_neuro(board, "O"):
        await callback_query.answer("Вы проиграли! Попробуйте еще раз.")
        for row in range(3):
            for col in range(3):
                if board[row][col] == "O":
                    board[row][col] = "O"
        await update_keyboard(callback_query.message)
        return

    if check_draw(board):
        await callback_query.answer("Ничья!")
        return

    await update_keyboard(callback_query.message)

def check_winner_neuro(board, symbol):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == symbol:
            return True

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == symbol:
            return True

    if board[0][0] == board[1][1] == board[2][2] == symbol:
        return True
    if board[0][2] == board[1][1] == board[2][0] == symbol:
        return True

    return False


def check_draw(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False
    return True


def make_computer_move(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = "O"
                if check_winner_neuro(board, "O"):
                    return row, col
                board[row][col] = " "

    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = "X"
                if check_winner_neuro(board, "X"):
                    return row, col
                board[row][col] = " "

    while True:
        row = randint(0, 2)
        col = randint(0, 2)
        if board[row][col] == " ":
            return row, col


async def update_keyboard(message: Message):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for row in range(3):
        buttons_row = []
        for col in range(3):
            button_text = board[row][col] if board[row][col] != " " else "-"
            buttons_row.append(
                InlineKeyboardButton(button_text,
                                           callback_data=f'move {row} {col}'))
        keyboard.add(*buttons_row)
    keyboard.add(
        InlineKeyboardButton("Играть снова", callback_data='reset'))

    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=message.message_id,
                                text=message.text,
                                reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'reset')
async def reset_game(callback_query: CallbackQuery):
    global board
    reset_board()
    board = [[" " for _ in range(3)] for _ in range(3)]
    await update_keyboard(callback_query.message)
    await callback_query.answer("Игра сброшена. Начните заново.")

