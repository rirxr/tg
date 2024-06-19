from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import BoundFilter
from datetime import datetime
from utils.cjson import load
import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] %(chattype)s %(username)s > %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

handler.setFormatter(formatter)

logger.addHandler(handler)

class IsPrivate(BoundFilter):
    async def check(self, message: Message):
        return message.chat.type == ChatType.PRIVATE
    
class IsGroup(BoundFilter):
    async def check(self, message: Message, *args) -> bool:
        return message.chat.type in [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]
    
async def log(message: Message):
    if await IsGroup().check(message):
        chattype = f'(CHAT - {message.chat.title})'
    elif await IsPrivate().check(message):
        chattype = '(PM)'

    id = message.from_user.id
    data = load(id)

    with open(f'logs/{datetime.now().strftime("%Y-%m-%d")}.log', "a") as file:
        file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {chattype} {message.from_user.username if message.from_user.username is not None else id} > {message.text}" + "\n")

    logger.info(message.text, extra={'username': message.from_user.username if message.from_user.username is not None else id, 'chattype': chattype})

    if data['name'] is None or data['lastname'] is None:
        return False
    else:
        return True