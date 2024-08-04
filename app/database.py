from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis


MONGO_DETAILS = "mongodb://localhost:27017"
REDIS_DETAILS = "redis://localhost:6379"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.messages
message_collection = database.get_collection("messages")

redis_client = None


async def get_database():
    return message_collection


async def get_redis():
    global redis_client
    if not redis_client:
        redis_client = await redis.from_url(REDIS_DETAILS)
    return redis_client
