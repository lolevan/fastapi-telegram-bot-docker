from pydantic import BaseModel


class Message(BaseModel):
    content: str
    author: str


class MessageResponse(BaseModel):
    id: str
    content: str
    author: str
    timestamp: int
