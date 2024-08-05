import os
import logging
import redis
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
WEB_APP_URL = os.getenv('WEB_APP_URL')
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

logging.basicConfig(level=logging.INFO)

# Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

bot = Bot(token=API_TOKEN)
storage = RedisStorage.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
dp = Dispatcher(storage=storage)


class Form(StatesGroup):
    message_content = State()


@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message):
    await message.reply("Hi!\nI'm your bot!")


@dp.message(Command(commands=['messages']))
async def get_messages(message: Message, state: FSMContext):
    cached_messages = redis_client.get('messages')
    if cached_messages:
        await message.reply(cached_messages)
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{WEB_APP_URL}/api/v1/messages/') as resp:
                messages = await resp.json()
                redis_client.set('messages', str(messages))
                await message.reply(str(messages))


@dp.message(Command(commands=['new_message']))
async def new_message(message: Message, state: FSMContext):
    await message.reply("Введите текст нового сообщения:")
    await state.set_state(Form.message_content)


@dp.message(Form.message_content)
async def process_new_message(message: Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        data = {
            "content": message.text,
            "author": message.from_user.username
        }
        async with session.post(f'{WEB_APP_URL}/api/v1/message/', json=data) as resp:
            response = await resp.json()
            redis_client.delete('messages')  # Invalidate cache
            await message.reply(str(response))
    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
