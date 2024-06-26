from aiogram.types import BotCommand
import math

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand("ai", "Задать вопрос нейросети."),
        BotCommand("duel", "Начать игру в 'Дуэль'"),
        BotCommand("guess", "Начать игру в 'Угадай слово'"),
        BotCommand("xo", "Начать игру в крестики-нолики."),
        BotCommand("xoo", "Начать игру в крестики-нолики с кем-то."),
        BotCommand("rps", "Начать игру в КНБ."),
        BotCommand("arrest", "арестовать кого-то"),
        BotCommand("blowup", "взорвать кого-то"),
        BotCommand("bury", "закопать кого-то"),
        BotCommand("chopoff", "отрубить кому-то что-то"),
        BotCommand("castrate", "кастрировать кого-то"),
        BotCommand("destroy", "уничтожить кого-то"),
        BotCommand("digout", "выкопать яму для кого-то"),
        BotCommand("drink", "выпить вместе с кем-то"),
        BotCommand("flogged", "выпороть кого-то"),
        BotCommand("force", "заставить кого-то"),
        BotCommand("fuck", "выебать кого-то"),
        BotCommand("hangup", "повесить кого-то"),
        BotCommand("humiliate", "унизить кого-то"),
        BotCommand("laugh", "рассмешить кого-то"),
        BotCommand("offer", "предложить кому-то что-то"),
        BotCommand("punish", "наказать кого-то"),
        BotCommand("sell", "продать кого-то"),
        BotCommand("shootoff", "отстрелить кого-то"),
        BotCommand("stagger", "ушатать кого-то"),
        BotCommand("suck", "засосать кого-то"),
        BotCommand("swear", "шмальнуть в кого-то"),
        BotCommand("tear", "порвать кого-то"),
        BotCommand("tickle", "щекотать кого-то"),
        BotCommand("tie", "связать кого-то"),
        BotCommand("wish", "пожелать кому-то что-то"),
        BotCommand("yell", "наорать на кого-то"),
    ])