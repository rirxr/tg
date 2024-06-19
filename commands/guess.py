import json
import os

from navec import Navec

import requests
import navec

from random import choice
from zipfile import ZipFile
from tqdm import tqdm
from pathlib import Path
from gensim.models import KeyedVectors
from handlers.log import log
from utils.loader import dp, bot
from aiogram.types import Message, ContentType, Chat, User, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import link

model_dir = Path("./models")
out_dir = Path("./games/guess_words")
out_name = str((i for i in range(99999) if not os.path.exists(f"./games/guess_words/{str(i)}.json")).__next__())

model_dir.mkdir(parents=True, exist_ok=True)
out_dir.mkdir(parents=True, exist_ok=True)
assert out_dir.is_dir() is True

noun_only_model_txt = model_dir / "noun_model.txt"

if noun_only_model_txt.exists() is False:

    zip_path = model_dir / "182.zip"
    response = requests.get("http://vectors.nlpl.eu/repository/20/182.zip", stream=True)
    with zip_path.open("wb") as f:
        for data in tqdm(response.iter_content(chunk_size=4*1024*1024), total=153):
            f.write(data)

    with ZipFile(zip_path) as archive:
        archive.extractall(model_dir)

    navec_model_tar = model_dir / "navec_hudlit_v1_12B_500K_300d_100q.tar"
    response = requests.get("https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar", stream=True)
    with navec_model_tar.open("wb") as f:
        for data in tqdm(response.iter_content(chunk_size=4*1024*1024), total=13):
            f.write(data)

    navec = Navec.load(navec_model_tar)

    original_model_txt = model_dir / "model.txt"

    nouns = []
    
    with original_model_txt.open("r", encoding="utf-8") as f:
        for line in tqdm(f, total=185925):
            if "_NOUN" not in line or "::" in line:
                continue

            clear_line = line.replace("_NOUN", "")
            clear_word = line.split('_')[0].strip()

            if "-" in clear_word:
                continue

            if clear_word not in navec:
                print(f"Strange word: {clear_word}")
                continue

            nouns.append(clear_line)

    with noun_only_model_txt.open("w", encoding="utf-8") as f:
        f.write(f"{len(nouns)} 300\n")
        for line in nouns:
            f.write(line)

model = KeyedVectors.load_word2vec_format(noun_only_model_txt, binary=False)

def find_max_json_file(folder_path):
    max_number = -1
    max_json_file = None

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_number = int(file_name.split(".")[0])
            if file_number > max_number:
                max_number = file_number
                max_json_file = file_name

    return max_json_file

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data
    
def get_random_line(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        random_line = choice(lines)
        return random_line.strip()
    
def create_dictionary(out_dir: Path, filename: str):
    out_txt_file: Path = out_dir / f"{filename}.txt"
    out_json_file: Path = out_dir / f"{filename}.json"
    word = get_random_line("./games/guess_words/0.txt")
    words = {
        word: 0
    }

    with out_txt_file.open("w", encoding="utf-8") as f:
        f.write(f"{word}\n")

        for i, (similar_word, _) in enumerate(model.most_similar(positive=[word], topn=50000), 1):
            f.write(f"{similar_word}\n")
            words[similar_word] = i

    with out_json_file.open("w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False)

inputed_words = []
players = []

class GuessState(StatesGroup):
    WaitingForGuess = State()
    
async def get_state():
    temp_message = Message(message_id=0, chat=Chat(id=0, type="private"), from_user=User(id=0))
    state = FSMContext.get_state(chat=temp_message.chat, user=temp_message.from_user)
    return state

def guess_join():
    jlpanel = InlineKeyboardMarkup()
    jbutton = InlineKeyboardButton("Присоединиться", callback_data="xjg")
    lbutton = InlineKeyboardButton("Выйти", callback_data="lxg")
    jlpanel.add(jbutton, lbutton)
    return jlpanel

@dp.callback_query_handler(lambda c: c.data == "xjg", state='*')
async def handle_join(call: CallbackQuery):
    global players
    if call.from_user.id not in players:
        players.append(call.from_user.id)
        name = link(call.from_user.full_name, f"https://t.me/{call.from_user.username}")
        state = dp.current_state(user=call.from_user.id)
        await bot.send_message(call.message.chat.id, f"Игрок {name} присоединился к игре.", disable_web_page_preview=True)
        await GuessState.WaitingForGuess.set()
        await state.update_data(user_id=players)
        return
    
    await call.answer("Вы и так находитесь в игре.")

@dp.callback_query_handler(lambda c: c.data == "lxg", state='*')
async def handle_leave(call: CallbackQuery):
    global players
    if call.from_user.id in players:
        players.remove(call.from_user.id)
        state = dp.current_state(user=call.from_user.id)
        name = link(call.from_user.full_name, f"https://t.me/{call.from_user.username}")
        await bot.send_message(call.message.chat.id, f"Игрок {name} вышел из игры.", disable_web_page_preview=True)
        await GuessState.WaitingForGuess.set()
        await state.update_data(user_id=players)
        return

    await call.answer("Вы не находитесь в игре.")

@dp.message_handler(commands=["guess"])
async def handle_guess_command(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)

    global players, inputed_words
    inputed_words.clear()
    players.clear()
    players.append(message.from_user.id)
    create_dictionary(out_dir, out_name)
    state = dp.current_state(user=message.from_user.id)
    await message.answer("Слово загадано. Начинайте угадывать.\n\nЕсли захотите выйти - /сдаться")
    await GuessState.WaitingForGuess.set()
    await state.update_data(user_id=message.from_user.id)

@dp.message_handler(state=GuessState.WaitingForGuess, content_types=ContentType.TEXT)
async def handle_guess(message: Message, state: FSMContext):
    global players
    user_data = await state.get_data()
    expected_user_id = user_data.get("user_id")
    json_data = load_json(f"./games/guess_words/{find_max_json_file('./games/guess_words/')}")
    
    if message.from_user.id not in players:
        return

    if message.text == "/сдаться":
        first_key, first_value = next(iter(json_data.items()))
        await message.answer(f"Загаданное слово: {first_key}")
        await state.reset_data()
        await state.reset_state()
        await state.finish()
        return

    guess_id = message.text.lower()
    
    if guess_id not in json_data:
        return await message.answer(f"Я не знаю слова {guess_id} :(")

    if guess_id in inputed_words:
        return await message.answer(f"Слово {guess_id} уже было использовано.")
        
    if json_data[guess_id] == 0:
        await message.answer(f"Вы угадали слово!\n\nЗагаданное слово было {guess_id}")
        await state.reset_data()
        await state.reset_state()
        await state.finish()
        return 
    
    if guess_id not in inputed_words and guess_id in json_data:
        inputed_words.append([guess_id, json_data[guess_id]])
        inputed_words.sort(key=lambda x: x[1])
        formatted_list = "\n".join([f"<b>{item[0]}</b> <i>({item[1]})</i>" for item in inputed_words])

        return await message.answer(f"Угадай слово\n\nПопытка: {len(inputed_words)}\n\nПоследнее введенное слово: {guess_id}\n\nРанее:\n{formatted_list}", reply_markup=guess_join(), parse_mode=ParseMode.HTML)
