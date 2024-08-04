from motor.motor_asyncio import AsyncIOMotorClient
import aioredis


MONGO_DETAILS = "mongodb://localhost:27017"
REDIS_DETAILS = "redis://localhost:6379"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.messages
message_collection = database.get_collection("messages")

redis = None


async def get_database():
    return message_collection


async def get_redis():
    global redis
    if not redis:
        redis = await aioredis.create_redis_pool(REDIS_DETAILS)
    return redis
