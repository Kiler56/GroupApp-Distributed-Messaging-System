from pydantic import BaseModel, Field
from typing import Literal

class Message(BaseModel):
    chat_id: str
    type: Literal["text", "image", "file"]
    content: str


class ReadRequest(BaseModel):
    user_id: str