import asyncio
import json
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

FILEPATH = "./data.json"
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()

discounts = []


def init():
    try:
        global discounts
        f = open(FILEPATH, "r")
        discounts = json.load(f)
        f.close()
        return True
    except IOError:
        print(f"{FILEPATH} is not available")
        return False

@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(f"Available commands: /support - support /discounts - see all discounts")


@dp.message(Command("support"))
async def support_handler(message: Message) -> None:
    await message.answer(f"Write to email: discount-bot@mail.ru")


@dp.message(Command("discounts"))
async def support_handler(message: Message) -> None:
    for discount in discounts[:10]:
        await message.answer(f"{discount['type']} {discount['description']} {discount['discount']} {discount['price']}")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    if init():
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
