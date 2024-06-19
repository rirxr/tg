from utils.commands import set_default_commands

async def on_startup(dp):
    await set_default_commands(dp)

if __name__ == '__main__':
    from aiogram import executor
    from start import dp
    # from utils.handlers import reg_handler
    # reg_handler()
    executor.start_polling(dp, on_startup=on_startup)
