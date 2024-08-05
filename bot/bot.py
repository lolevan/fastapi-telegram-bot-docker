import os
import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
WEB_APP_URL = os.getenv('WEB_APP_URL')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Form(StatesGroup):
    message_content = State()


@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm your bot!")


@dp.message(Command(commands=['messages']))
async def get_messages(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{WEB_APP_URL}/api/v1/messages/') as resp:
            messages = await resp.json()
            response = "\n".join([f"{msg['author']}: {msg['content']}" for msg in messages])
            await message.reply(response)


@dp.message(Command(commands=['new_message']))
async def new_message(message: types.Message, state: FSMContext):
    await state.set_state(Form.message_content)
    await message.reply("Введите текст нового сообщения:")


@dp.message(F.state == Form.message_content)
async def process_message_content(message: types.Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        data = {
            "content": message.text,
            "author": message.from_user.username
        }
        async with session.post(f'{WEB_APP_URL}/api/v1/message/', json=data) as resp:
            response = await resp.json()
            await message.reply(str(response))
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
