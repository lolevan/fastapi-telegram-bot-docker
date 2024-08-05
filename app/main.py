from fastapi import FastAPI, Depends
from typing import List
from database import get_database, get_redis
from crud import get_messages, create_message
from schemas import Message, MessageResponse
import uvicorn

app = FastAPI()


@app.get("/api/v1/messages/", response_model=List[MessageResponse])
async def read_messages(db=Depends(get_database), redis=Depends(get_redis)):
    messages = await get_messages(db, redis)
    return messages


@app.post("/api/v1/message/", response_model=MessageResponse)
async def post_message(message: Message, db=Depends(get_database), redis=Depends(get_redis)):
    return await create_message(db, redis, message)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
