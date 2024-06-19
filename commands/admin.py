from handlers.log import log
from utils.cjson import load, loaduser
from utils.loader import dp
from aiogram.types import Message
from aiogram.utils.markdown import link
import os, json

@dp.message_handler(commands=['admin', 'adm'])
async def admin(message: Message):
    if not await log(message):
        await log(message)
        return await message.answer("Вы не можете использовать бота, поскольку не завершили регистрацию.\n\nДля завершения регистрации, введите в ЛС бота команду /reg и следуйте дальнейшим указаниям.")
    else:
        await log(message)

    msg = message.text.split()
    selfdata = load(message.from_user.id)

    if len(msg) <= 1:
        return await message.answer('Вы не указали аргумент.\n\nДоступные аргументы:\n[ * ] add - добавить админа\n[ * ] rem (remove, del, delete) - удалить админа\n[ * ] ls (list) - посмотреть список админов')
    
    try:
        if msg[1] not in ['ls', 'list']:
            data = load(message.reply_to_message.from_user.id)
            target = link(message.reply_to_message.from_user.full_name, f"https://t.me/{message.reply_to_message.from_user.username}")
    except AttributeError:
        try:
            if msg[1] not in ['ls', 'list']:
                data = loaduser(msg[2].replace('@', ''))
                target = link(msg[2].replace('@', ''), f"https://t.me/{msg[2].replace('@', '')}")
                
                if data is None:
                    return await message.reply(f'Пользователь {target} не найден в базе данных.\nЗаставьте его написать хоть что-нибудь.', disable_web_page_preview=True)
        except IndexError:
            await message.answer('Вы не указали пользователя.\n\nДля этого достаточно переслать его сообщение или написать айди после команды.')
    
    async def notPerm():
        if not selfdata['admin']:
            return await message.reply('У Вас нет прав на использование этой команды.')
    
    async def userNotFound(data):
        if not data['id']:
            return await message.reply(f'Пользователь {target} не найден в базе данных.\nЗаставьте его написать хоть что-нибудь.', disable_web_page_preview=True)
    
    async def alreadyAdmin(data):
        if data['admin']:
            return await message.answer(f'Пользователь {target} и так является админом.', disable_web_page_preview=True)
        
    async def notAdmin(data):
        if not data['admin']:
            return await message.answer(f'Пользователь {target} и так не является админом.', disable_web_page_preview=True)
    
    async def afterData(data):
        with open(f'./users/{data["id"]}.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    if msg[1] == 'add':
        if await notPerm():
            return
        
        if await userNotFound(data):
            return
        
        if await alreadyAdmin(data):
            return

        data['admin'] = True
        await afterData(data)

        await message.answer(f'Пользователь {target} теперь админ.', disable_web_page_preview=True)
    
    if msg[1] in ['rem', 'remove', 'del', 'delete']:
        if await notPerm():
            return
        
        if await userNotFound(data):
            return
        
        if await notAdmin(data):
            return
        
        data['admin'] = False
        await afterData(data)
        
        await message.answer(f'Пользователь {target} теперь не админ.', disable_web_page_preview=True)

    if msg[1] in ['list', 'ls']:
        admins = []

        for file in os.listdir('./users'):
            admin = load(file.replace('.json', ''))

            if admin['admin']:
                admins.append(link(admin['username'], f'https://t.me/{admin["username"]}'))

        adms = '\n- '.join(admins)
        await message.answer(f'Список админов бота:\n\n- {adms}', disable_web_page_preview=True)