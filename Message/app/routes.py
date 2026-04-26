from fastapi import APIRouter, Depends
from app.models import Message, ReadRequest
from app.services import create_message, get_messages, mark_message_as_read
from app.auth import get_current_user

router = APIRouter()

@router.post("/messages/send")
def send_message(message: Message, user=Depends(get_current_user)):
    return create_message(message, user)


@router.get("/messages/{chat_id}")
def read_messages(
    chat_id: str,
    limit: int = 50,
    skip: int = 0,
    user=Depends(get_current_user)
):
    return get_messages(chat_id, limit, skip, user)

@router.put("/messages/{message_id}/read")
def mark_as_read(message_id: str, user=Depends(get_current_user)):
    return mark_message_as_read(message_id, user["id"])