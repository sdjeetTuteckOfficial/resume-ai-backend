from fastapi import WebSocket
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        # Store active connections: { "user_id": WebSocket }
        self.active_connections: Dict[str, WebSocket] = {}
        # Store admin connections: List[WebSocket]
        self.admin_connections: List[WebSocket] = []

    async def connect_user(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"✅ Candidate Connected: {user_id}")
        
        # Notify admins that a new user is online
        await self.broadcast_to_admins({
            "type": "user-list-update",
            "users": list(self.active_connections.keys())
        })

    async def connect_admin(self, websocket: WebSocket):
        await websocket.accept()
        self.admin_connections.append(websocket)
        print(f"🛡️ Admin Connected. Total Admins: {len(self.admin_connections)}")
        
        # Send current user list to the new admin immediately
        await websocket.send_json({
            "type": "user-list-update",
            "users": list(self.active_connections.keys())
        })

    def disconnect_user(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"❌ Candidate Disconnected: {user_id}")
    
    def disconnect_admin(self, websocket: WebSocket):
        if websocket in self.admin_connections:
            self.admin_connections.remove(websocket)
            print("❌ Admin Disconnected")

    async def broadcast_to_admins(self, message: dict):
        # iterate over copy to avoid runtime errors if list changes
        for connection in self.admin_connections.copy(): 
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to admin: {e}")
                self.disconnect_admin(connection)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")

# Create a global instance to be imported by the router
socket_manager = ConnectionManager()