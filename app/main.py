from fastapi import FastAPI, Depends
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
import aioredis

from app.database import get_database, get_redis
from app.crud import get_messages, create_message
from app.schemas import Message, MessageResponse

app = FastAPI()


@app.get('/api/v1/messages/', response_model=List[MessageResponse])
async def read_messages(
    db: AsyncIOMotorClient = Depends(get_database),
    redis: aioredis.Redis = Depends(get_redis),
):
    messages = await get_messages(db, redis)
    return messages


@app.post('/api/v1/message/', response_model=MessageResponse)
async def post_message(
    message: Message,
    db: AsyncIOMotorClient = Depends(get_database),
    redis: aioredis.Redis = Depends(get_redis),
):
    message = await create_message(db, redis, message)
    return message
