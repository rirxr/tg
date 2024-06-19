from handlers.log import log
from utils.cjson import load, dump
from utils.loader import dp
from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
import json, os

class NotCommand(BoundFilter):
    async def check(self, message: Message):
        if not message.text.startswith('/'):
            return True

@dp.message_handler(NotCommand())
async def reg(message: Message):
    if not os.path.exists(f'./users/{message.from_user.id}.json'):
        with open(f'./users/{message.from_user.id}.json', 'w') as f:
            json.dump({
                "name": None,
                "lastname": None,
                "username": message.from_user.username,
                "id": message.from_user.id,
                "admin": False
            }, f, indent=4)
    elif message.from_user.username != load(message.from_user.id)['username']:
        load(message.from_user.id)['username'] = message.from_user.username

    await log(message)