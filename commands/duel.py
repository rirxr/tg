from handlers.log import log
from utils.loader import dp, bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import link
from random import randint, choice


players = {}

@dp.message_handler(commands=['duel', 'дуэль'])
async def start_duel(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)

    global players
    if not message.reply_to_message:
        return await message.reply("Пожалуйста, укажите пользователя, с которым вы хотите сыграть в дуэль.")
        
    if message.reply_to_message.from_user.username == message.from_user.username:
        return await message.reply("Суицидник, что ли? Выбери другого участника.")
        
    players = {
        'player1': message.from_user.username,
        'player2': message.reply_to_message.from_user.username, 
        'current_player': message.from_user.username,
        'opponent': link(message.reply_to_message.from_user.full_name, f'https://t.me/{message.reply_to_message.from_user.username}'),
        'org': link(message.from_user.full_name, f'https://t.me/{message.from_user.username}'),
        'hp': {
            message.from_user.username: 100, 
            message.reply_to_message.from_user.username: 100
        }
    }

    if not players['player2']:
        await message.reply("К сожалению, я не могу получить информацию о пользователе.")
        return

    confirmation_kb = InlineKeyboardMarkup()
    accept_button = InlineKeyboardButton("Принять", callback_data="accept")
    decline_button = InlineKeyboardButton("Отказаться", callback_data="decline")
    confirmation_kb.add(accept_button, decline_button)

    await message.reply(f"{players['opponent']}, вас вызывают на дуэль! Принимаете вызов?", reply_markup=confirmation_kb, disable_web_page_preview=True)

@dp.callback_query_handler(lambda c: c.data == "accept")
async def handle_confirmation(call: CallbackQuery):
    global players
    if call.from_user.username == players['player2']:
        await call.answer("Вы приняли вызов! Приготовьтесь к дуэли.")
        player_id = call.from_user.id
        players[player_id] = 100
        await bot.send_message(call.message.chat.id, "Дуэль началась! Вы начинаете с 100 хп.")
        await bot.send_message(call.message.chat.id, f"Ход {players['org']}. Выстрелите!", reply_markup=get_shoot_kb(), disable_web_page_preview=True)
    elif call.from_user.username == players['player1']:
        await call.answer("Вы организатор дуэли, поэтому Вам не нужно приглашение.")
    else:
        await call.answer("Вас не приглашали на дуэль.")

@dp.callback_query_handler(lambda c: c.data == "decline")
async def handle_confirmation(call: CallbackQuery):
    global players
    if call.from_user.username == players['player2']:
        await bot.edit_message_reply_markup.answer("Вы отказались от вызова.")
    elif call.from_user.username == players['player1']:
        await call.answer("Струсил, что ли? Поздно отступать.")
    else:
        await call.answer("Вас не приглашали на дуэль.")

def get_shoot_kb():
    shoot_kb = InlineKeyboardMarkup()
    shoot_button = InlineKeyboardButton("Выстрелить", callback_data="shoot")
    shoot_kb.add(shoot_button)
    return shoot_kb

@dp.callback_query_handler(lambda c: c.data == "shoot")
async def handle_shoot(call: CallbackQuery):
    global players
    player_id = call.from_user.username
    player_hp = players['hp'][player_id]
    if player_hp <= 0:
        return await call.answer("Вы уже проиграли!")
    
    if call.from_user.username == players['player1']:
        first = players['org']
        second = players['opponent']
    elif call.from_user.username == players['player2']:
        first = players['opponent']
        second = players['org']

    name = link(call.from_user.full_name, f"https://t.me/{call.from_user.username}")

    if call.from_user.username == players['current_player']:
        is_missed = choice([True, False])
        if is_missed:
            await bot.send_message(call.message.chat.id, f"{name} стреляет и...\n\nПромахивается!", reply_markup=get_shoot_kb(), disable_web_page_preview=True)

            if players['current_player'] == players['player1']:
                players['current_player'] = players['player2']
            else:
                players['current_player'] = players['player1']
        else:
            damage = randint(30, 100)
            opponent_hp = players['hp'][player_id]

            if opponent_hp <= 0:
                await bot.send_message(call.message.chat.id, f"{name} победил!", disable_web_page_preview=True)
                return

            opponent_hp -= damage
            players['hp'][player_id] = opponent_hp

            if players['current_player'] == players['player1']:
                players['current_player'] = players['player2']
            else:
                players['current_player'] = players['player1']

            if opponent_hp <= 0:
                await bot.send_message(call.message.chat.id, f"{first} попал и нанес {damage} урона! У {second} не осталось хп. \n{first} победил.", disable_web_page_preview=True)
                players.clear()
            else:

                await bot.send_message(call.message.chat.id, f"{first} попал и нанес {damage} урона! {second} имеет {opponent_hp} хп.", disable_web_page_preview=True)
                await bot.send_message(call.message.chat.id, f"Ход {second}. Ожидайте его выстрела...", reply_markup=get_shoot_kb(), disable_web_page_preview=True)
    else:
        await call.answer("Сейчас не Ваш ход.")
