from .loader import dp
from commands import dp as commands_dp
from handlers import dp as handlers_dp
from aiogram.types import ContentTypes
import os

def reg_handler():
    dp.middleware.setup(commands_dp)
    dp.middleware.setup(handlers_dp)