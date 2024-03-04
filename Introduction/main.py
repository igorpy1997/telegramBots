import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode

TOKEN = ""


dp = Dispatcher()



@dp.message()
async def echo_handler(message: types.Message):
    await message.answer("Hello")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())