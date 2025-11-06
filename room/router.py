from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/ws", response_class=HTMLResponse)
async def web_sockets(request:Request):
    return templates.TemplateResponse(
        request=request,
        name='ws.html'
    )


class ActiveConnection:
    def __init__(self, websocket, room_code):
        self.websocket:WebSocket = websocket
        self.room_code:int = room_code
        

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[ActiveConnection] = []

    async def connect(self, websocket: WebSocket, room_code:int):
        await websocket.accept()
        active = ActiveConnection(websocket, room_code)
        self.active_connections.append(active)

    def remove_connection(self, connection: ActiveConnection, websocket:WebSocket):
        return connection.websocket != websocket

    def disconnect(self, websocket: WebSocket):
        self.active_connections = list(filter(lambda connection: self.remove_connection(connection, websocket), self.active_connections))

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, room_code:int):
        for connection in self.active_connections:
            if connection.room_code == room_code:
                await connection.websocket.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{client_id}/{room_code}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, room_code:int):
    await manager.connect(websocket, room_code)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}", room_code)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", room_code)