from handlers.log import log
from utils.loader import dp, bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import link

player1 = None
player2 = None
games = {}
game_id = 0

board = [[" " for _ in range(3)] for _ in range(3)]

def reset_board():
    global board
    board = [[" " for _ in range(3)] for _ in range(3)]

@dp.message_handler(commands=['xoo'])
async def start_game_xoo(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)

    global player1, player2
    player2 = message.text.replace("/xo", "").strip()
    games[game_id] = {
        'player1': message.from_user.id,
        'player2': None,
        'board': [[' ' for _ in range(3)] for _ in range(3)],
        'turn': 'X',
        'current_player': message.from_user.id,
        'player2_name': None,
    }

    keyboard = InlineKeyboardMarkup(row_width=1)
    join_button = InlineKeyboardButton("Присоединиться",
                                                callback_data="join")
    keyboard.add(join_button)
    await message.answer("          <b>Крестики-нолики\nРежим игры: С другим игроком</b>",
                            reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('join'))
async def join_game(callback_query: CallbackQuery):
    if callback_query.from_user.id == games[game_id]['player1']:
        await callback_query.answer(
            "Вы не можете присоединиться к самому себе!")
        return

    if game_id in games and games[game_id]['player2'] is None:
        games[game_id]['player2'] = callback_query.from_user.id
        games[game_id][
            'player2_name'] = 'С @' + callback_query.from_user.username
        await bot.send_message(
            callback_query.message.chat.id,
            "Вы присоединились к игре. Первый игрок сделает ход.")
        await update_keyboard(callback_query.message)
    else:
        await bot.send_message(callback_query.from_user.id,
                               "Вы не участвуете в игре или игра уже начата.")


async def check_participation(user_id):
    if user_id == player1 or user_id == player2:
        return True
    else:
        return False
    
@dp.callback_query_handler(lambda c: c.data.startswith('nmove'))
async def make_move(callback_query: CallbackQuery):
    global player1, player2
    row, col = map(int, callback_query.data.split()[1:])

    player1 = games[game_id]['player1']
    player2 = games[game_id]['player2']

    if board[row][col] != " ":
        await callback_query.answer("Эта клетка уже занята.",
                                    show_alert=True)
        return

    if callback_query.from_user.id != games[game_id]['current_player']:
        await callback_query.answer("Сейчас не ваш ход.", show_alert=True)
        return

    if callback_query.from_user.id == player1:
        symbol = "X"
    elif callback_query.from_user.id == player2:
        symbol = "O"
    else:
        user_id = callback_query.from_user.id
        participating = await check_participation(user_id)
        if not participating:
            await callback_query.answer("Вы не участвуете в игре.",
                                        show_alert=True)
            return

    board[row][col] = symbol

    if games[game_id]['current_player'] == games[game_id]['player1']:
        games[game_id]['current_player'] = games[game_id]['player2']
    else:
        games[game_id]['current_player'] = games[game_id]['player1']

    if check_winner(board, symbol):
        name = link(callback_query.from_user.full_name, f'https://t.me/{callback_query.from_user.username}')
        await bot.send_message(
            callback_query.message.chat.id,
            f"Игрок {name} выиграл! Поздравляю!",
            disable_web_page_preview=True
        )
    elif check_draw(board):
        await bot.send_message(callback_query.message.chat.id, "Ничья!")
    else:
        await callback_query.answer()

    await update_keyboard(callback_query.message)

def check_winner(board, symbol):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == symbol:
            reset_board()
            board = [[" " for _ in range(3)] for _ in range(3)]
            return True

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == symbol:
            reset_board()
            board = [[" " for _ in range(3)] for _ in range(3)]
            return True

def check_draw(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False
    return True

async def update_keyboard(message: Message):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for row in range(3):
        buttons_row = []
        for col in range(3):
            button_text = board[row][col] if board[row][col] != " " else "-"
            buttons_row.append(
                InlineKeyboardButton(button_text,
                                           callback_data=f'nmove {row} {col}'))
        keyboard.add(*buttons_row)
    keyboard.add(
        InlineKeyboardButton("Играть снова", callback_data='nreset'))

    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=message.message_id,
                                text=message.text,
                                reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'nreset')
async def reset_game(callback_query: CallbackQuery):
    global board
    reset_board()
    board = [[" " for _ in range(3)] for _ in range(3)]
    await update_keyboard(callback_query.message)
    await callback_query.answer("Игра сброшена. Начните заново.")

