from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
import threading
import json
import asyncio
from app.rabbitmq import consume_messages
from typing import List, Dict

app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- WebSocket Management ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: str):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_id: str):
        if chat_id in self.active_connections:
            self.active_connections[chat_id].remove(websocket)

    async def broadcast(self, chat_id: str, message: dict):
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str):
    await manager.connect(websocket, chat_id)
    try:
        while True:
            await websocket.receive_text() # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)

# --- RabbitMQ to WebSocket Bridge ---
def rabbit_callback(ch, method, properties, body):
    event_data = json.loads(body)
    print("📩 Evento recibido de RabbitMQ:", event_data)
    
    if event_data.get("event") == "message_sent":
        data = event_data.get("data", {})
        chat_id = data.get("chat_id")
        
        # Enviar al bridge asíncrono
        if chat_id:
            asyncio.run_coroutine_threadsafe(
                manager.broadcast(chat_id, {"type": "new_message"}),
                loop
            )
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_rabbit_consumer():
    import pika
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
    channel = connection.channel()
    channel.queue_declare(queue="messages", durable=True)
    channel.basic_consume(queue="messages", on_message_callback=rabbit_callback)
    channel.start_consuming()

# Event Loop para el bridge
loop = asyncio.get_event_loop()
threading.Thread(target=start_rabbit_consumer, daemon=True).start()
