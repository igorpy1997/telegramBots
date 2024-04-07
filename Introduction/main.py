import asyncio
import json
import logging
import sys


from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import Command
from aiogram.types import Message, URLInputFile, ReactionTypeEmoji, FSInputFile




# ваш основний скрипт
from config import Token




dp = Dispatcher()
router = Router()
dp.include_router(router)

bot = Bot(Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@router.message(F.voice)
async def voice_handler(message: types.Message):
    await bot.send_voice(chat_id=message.chat.id, voice=message.voice.file_id)

@router.message(F.text == "Моє айді")
async def id_handler(message: types.Message):
    await message.answer(str(message.from_user.id))

@router.message(F.text == "Повідомлення")
async def voice_handler(message: types.Message):
    id = ""
    await bot.forward_message(chat_id=id, from_chat_id=message.chat.id, message_id=message.message_id)


@router.message(F.text == "Відправити голосове")
async def voice_handler(message: types.Message):
    voice_message = FSInputFile("voice_01-04-2024_17-28-09.ogg")
    await bot.send_voice(chat_id=message.chat.id, voice=voice_message)
    await message.answer("Тримай, друже!")

@router.message(F.text == "Hello")
async def hello_handler(message: types.Message):
    await message.answer("Hello. How are you?")


@router.message(F.text == "Bye")
async def hello_handler(message: types.Message):
    await message.answer("Bye-Bye. See you later.")


@router.message(F.text.lower().replace(" ", "") == "скиньменіфотоскомпа")
async def photo_handler(message: types.Message):
    photo = FSInputFile("Screenshot from 2024-03-21 10-45-28.png")
    await bot.send_photo(chat_id=message.chat.id, photo=photo)


@router.message(F.text == "Voice")
async def voice_handler(message: types.Message):
    audio = FSInputFile("just dance.mp3")
    await bot.send_voice(chat_id=message.chat.id, voice = audio)


@router.message(F.text == "Скинь пісню")
async def voice_handler(message: types.Message):
    audio = FSInputFile("just dance.mp3")
    await bot.send_audio(chat_id=message.chat.id, audio = audio)


@router.message(F.text == "Постав мені лайк")
async def set_react(message: types.Message):
    thumb_up_reaction = ReactionTypeEmoji(emoji='👍')

    # Передача цього екземпляра у список реакцій
    await bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id, reaction=[thumb_up_reaction])


@router.edited_message()
async def edited_message(message: types.Message):
    await message.answer(f"Message{message.message_id} was changed")


@router.message(F.text.contains("купити"))
async def echo_message(message: types.Message):
    Michaelsid = ""
    Maks_id =""
    await bot.forward_message(chat_id=Michaelsid, from_chat_id=message.chat.id, message_id=message.message_id)
    await bot.forward_message(chat_id=Maks_id, from_chat_id=message.chat.id, message_id=message.message_id)

@router.message(F.text == "Перешли повідомлення")
async def echo_message(message: types.Message):
    await message.forward(message.chat.id)

@router.message(F.text == "Скинь гіфку")
async def gifs_handler(message: types.Message):
    gif_url = "https://compote.slate.com/images/697b023b-64a5-49a0-8059-27b963453fb1.gif"
    await bot.send_animation(chat_id=message.chat.id, animation=gif_url)

@router.message(F.audio)
async def voice_handler(message: types.Message):
    await bot.send_audio(chat_id=message.chat.id, audio=message.audio.file_id)


@router.message(F.text == "Скинь фото")
async def photo_handler2(message: types.Message):
    image = URLInputFile(
        "https://a.cdn-hotels.com/gdcs/production29/d1870/6a5ec560-bb25-11e8-970b-0242ac110006.jpg?impolicy=fcrop&w=800&h=533&q=medium"

    )
    await bot.send_photo(chat_id=message.chat.id, photo=image)

@router.message(F.document)
async def photo_handler(message: types.Message):
    await message.answer("I recieved your document!")
    await bot.send_document(chat_id=message.chat.id, document=message.document.file_id)









async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
