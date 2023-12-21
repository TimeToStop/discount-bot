import asyncio
import json
import logging
import random
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

FILEPATH = "./data.json"
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

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
    await message.answer(f"Бот по рекоммендации скидок.\nВведите /discounts, чтобы получить новую подборку.")


@dp.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(f"Доступные команды:\n/support - поддержка\n/discounts - новая подборка\n/help - список команд")


@dp.message(Command("support"))
async def support_handler(message: Message) -> None:
    await message.answer(f"Email для связи: discount-bot@mail.ru")


@dp.message(Command("discounts"))
async def discounts_handler(message: Message) -> None:
    kb = [
        [
            types.KeyboardButton(text="Restaurants"),
            types.KeyboardButton(text="Health"),
            types.KeyboardButton(text="Beauty")
        ],
    ]
    await message.answer("Выберите категорию", reply_markup=types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите"
    ))


async def send_discount_card(discount, message: Message) -> None:
    await message.answer_photo(
        discount["picture"],
        caption=f"{discount['discount']} {discount['description']}\nЦена {discount['price']}",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="Ссылка", url=discount['link'])]
            ]
        )
    )


def get_random_5(_discounts, _type):
    collection = filter(lambda e: e['type'] == _type, _discounts)
    return random.choices(list(collection), k=5)


@dp.message(F.text == "Restaurants")
async def help_handler(message: Message) -> None:
    for discount in get_random_5(discounts, "restaurant"):
        await send_discount_card(discount, message)


@dp.message(F.text == "Health")
async def help_handler(message: Message) -> None:
    for discount in get_random_5(discounts, "health"):
        await send_discount_card(discount, message)


@dp.message(F.text == "Beauty")
async def help_handler(message: Message) -> None:
    for discount in get_random_5(discounts, "beauty"):
        await send_discount_card(discount, message)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    if init():
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
