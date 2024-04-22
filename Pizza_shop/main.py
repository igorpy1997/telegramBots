import asyncio
import json
import logging
import sys


from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, URLInputFile, ReactionTypeEmoji, FSInputFile, ReplyKeyboardRemove, \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State

# ваш основний скрипт
from config import Token




dp = Dispatcher()
router = Router()
storage = MemoryStorage()
dp.include_router(router)

bot = Bot(Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
image_url = "https://yumchief.com/wp-content/uploads/2020/07/classic-margarita-cocktail-main-min.jpg"

pizzas = [
    {"name": "Маргарита", "url": "https://lh3.googleusercontent.com/-F7-f2RyixFJ_0-MIGehlz7lp08CkWuy7Y64qDx8zcSrAyHA_uWVnJx1XOVAHg_qoFD7fW34aWScKlOz7tlHx8LeBxDoB64vaZ6LCKKMAPPnr8-QTpPpQVVK-xGPWFZomSVkVZXW"},
    {"name": "Пеппероні", "url": "https://aegpizza.ru/wp-content/uploads/2021/03/%D0%BF%D0%B5%D0%BF%D0%BF%D0%B5%D1%80%D0%BE%D0%BD%D0%B8-scaled.jpg"},
    {"name": "Гавайська", "url": "https://cdn.lifehacker.ru/wp-content/uploads/2021/01/1_1611130322-e1710884562989-1280x640.jpg"},
    {"name": "Чотири сири", "url": "https://adriano.com.ua/wp-content/uploads/2022/08/%D0%9F%D1%96%D1%86%D0%B0-4-%D1%81%D0%B8%D1%80%D1%83-%D1%8F%D0%BA-%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D1%8C%D0%BD%D0%BE-%D0%B7%D1%80%D0%BE%D0%B1%D0%B8%D1%82%D0%B8-%D1%81%D0%BC%D0%B0%D1%87%D0%BD%D1%83-%D1%81%D1%82%D1%80%D0%B0%D0%B2%D1%83.png"},
    {"name": "Вегетаріанська", "url": "https://papitospizza.ru/wa-data/public/shop/products/44/00/44/images/307/307.970.jpg"},
    {"name": "З морепродуктами", "url": "https://img.taste.com.au/JDi_goQG/taste/2016/11/seafood-dill-pizza-5236-1.jpeg"},
    {"name": "З беконом", "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGMfPFQNX0fKm4c7dkis0nnkRRr44JJXYF58gDk3JwZQ&s"},
    {"name": "Барбекю", "url": "https://www.thecandidcooks.com/wp-content/uploads/2023/04/bbq-chicken-pizza-feature.jpg"},
    {"name": "Карбонара", "url": "https://pizzeriavesuviana.pl/wp-content/uploads/2021/05/18.-Pizza-Carbonara-crop-e1621716523633.jpg"},
    {"name": "Спайсі", "url": "https://www.thecandidcooks.com/wp-content/uploads/2022/08/spicy-sausage-pepper-pizza-feature.jpg"}
]
user_data = {}


def get_pizza_menu(page=0):
    items_per_page = 3
    pages = len(pizzas) // items_per_page + (len(pizzas) % items_per_page > 0)

    first_item_index = page * items_per_page
    last_item_index = min(first_item_index + items_per_page, len(pizzas))

    buttons = []
    for pizza in pizzas[first_item_index:last_item_index]:
        buttons.append([InlineKeyboardButton(text=pizza["name"], callback_data=f"pizza_{pizza['name']}")])

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="<< Назад", callback_data=f"page_{page - 1}"))
    if page < pages - 1:
        navigation_buttons.append(InlineKeyboardButton(text="Вперед >>", callback_data=f"page_{page + 1}"))

    buttons.append([InlineKeyboardButton(text="Завершити замовлення", callback_data="finish_order")])


    if navigation_buttons:
        buttons.append(navigation_buttons)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def show_pizza_menu(message: types.Message, page=0):
    text_lines = []
    for pizza in pizzas[page * 3:(page + 1) * 3]:
        text_lines.append(f"{pizza['name']}\n[Картинка]({pizza['url']})")
    text = "\n\n".join(text_lines)
    await message.answer_photo(photo=pizzas[page * 3]['url'], caption=text, reply_markup=get_pizza_menu(page),
                               parse_mode='Markdown')


@router.message(Command("order"))
async def cmd_start(message: types.Message):
    user_data[message.from_user.id] = {'order': []}
    await show_pizza_menu(message)


@router.callback_query()
async def on_callback_query(callback_query: types.CallbackQuery):
    user_order = user_data[callback_query.from_user.id]['order']
    data = callback_query.data

    if data.startswith("pizza"):
        pizza_name = data.split("_")[1]
        user_order.append(pizza_name)
        await callback_query.message.answer(f"Вы додали {pizza_name} в ваш замовлення.")
    elif data.startswith("page"):
        page = int(data.split("_")[1])
        await callback_query.message.delete()
        await show_pizza_menu(callback_query.message, page)
    elif data == "finish_order":
        order_details = ", ".join(user_order)
        await callback_query.message.answer(f"Ваше замовлення: {order_details}. Дякуємо за покупку!")
        await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())