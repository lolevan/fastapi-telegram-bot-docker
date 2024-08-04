from aiogram import Bot, Dispatcher, types
import asyncio
import aiohttp
import os
import logging

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
WEB_APP_URL = os.getenv('WEB_APP_URL')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm your bot!")


@dp.message_handler(commands=['messages'])
async def get_messages(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{WEB_APP_URL}/api/v1/messages/') as resp:
            messages = await resp.json()
            await message.reply(str(messages))


@dp.message_handler(commands=['new_message'])
async def new_message(message: types.Message):
    async with aiohttp.ClientSession() as session:
        data = {
            "content": message.text.split('/new_message ', 1)[1],
            "author": message.from_user.username
        }
        async with session.post(f'{WEB_APP_URL}/api/v1/message/', json=data) as resp:
            response = await resp.json()
            await message.reply(str(response))


async def main():
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
