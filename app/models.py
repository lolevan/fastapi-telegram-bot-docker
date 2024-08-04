from pydantic import BaseModel


class MessageInDB(BaseModel):
    id: str
    content: str
    author: str
    timestamp: int
