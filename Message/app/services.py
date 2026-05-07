from app.database import messages_collection
from datetime import datetime
from bson import ObjectId
from app.rabbitmq import publish_event
from app.config import GRUPOS_SERVICE_URL

def create_message(data, user):
    user_id = user.get("user_id")

    # validar que pertenece al grupo
    if not user_in_group(user_id, data.chat_id, user.get("token")):
        return {"error": "No pertenece al grupo"}

    message = {
        "chat_id": data.chat_id,
        "sender_id": user_id,
        "type": data.type,
        "content": data.content,
        "timestamp": datetime.utcnow(),
        "status": {
            "delivered_to": [],
            "read_by": []
        }
    }

    # 💾 guardar en Mongo
    result = messages_collection.insert_one(message)
    message["_id"] = str(result.inserted_id)

    # 🐇 evento RabbitMQ
    publish_event("messages", {
        "event": "message_sent",
        "data": {
            "chat_id": data.chat_id,
            "sender_id": user_id
        }
    })

    return message


def get_messages(chat_id: str, limit: int = 50, skip: int = 0, user=None):
    user_id = user.get("user_id")

    if not user_in_group(user_id, chat_id, user.get("token")):
        return {"error": "No pertenece al grupo"}

    messages = list(
        messages_collection.find({"chat_id": chat_id})
        .sort("timestamp", -1)
        .skip(skip)
        .limit(limit)
    )

    for msg in messages:
        msg["_id"] = str(msg["_id"])

    return messages


def mark_message_as_read(message_id: str, user_id: str):
    try:
        object_id = ObjectId(message_id)
    except Exception as e:
        return {"error": str(e)}

    result = messages_collection.update_one(
        {"_id": object_id},
        {"$addToSet": {"status.read_by": user_id}}
    )

    publish_event("messages", {
        "event": "message_read",
        "data": {
            "message_id": message_id,
            "user_id": user_id
        }
    })

    return {"updated": result.modified_count}


def user_in_group(user_id: str, group_id: str, token: str):
    try:
        response = requests.get(
            f"{GRUPOS_SERVICE_URL}/users-groups/{group_id}/usuarios",
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code != 200:
            print("Error groups:", response.text)
            return False

        users = response.json()

        return any(str(u["id_usuario"]) == str(user_id) for u in users)

    except Exception as e:
        print("Error en user_in_group:", e)
        return False