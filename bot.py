import os
import asyncio
import logging

from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from common import user_commands
from handlers.user_private import user_router

ALLOWED_UPDATES = ['message', 'callback_query']


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=user_commands.USER_CMDS)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':
    asyncio.run(main())
