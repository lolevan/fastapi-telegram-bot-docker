from models import MessageInDB
from schemas import Message
from datetime import datetime
import json


async def get_messages(db, redis):
    cached_messages = await redis.get("messages")
    if cached_messages:
        return json.loads(cached_messages)
    messages = []
    async for message in db.find():
        messages.append(MessageInDB(**message))
    await redis.set("messages", json.dumps([message.dict() for message in messages]))
    return messages


async def create_message(db, redis, message: Message):
    message_data = message.dict()
    message_data["timestamp"] = int(datetime.utcnow().timestamp())
    result = await db.insert_one(message_data)
    created_message = MessageInDB(id=str(result.inserted_id), **message_data)
    await redis.delete("messages")
    return created_message
