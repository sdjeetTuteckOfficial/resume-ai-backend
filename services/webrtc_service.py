from fastapi import WebSocket
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        # Stores active candidate connections: { "user_id": WebSocket }
        self.active_connections: Dict[str, WebSocket] = {}
        # Stores active admin connections: List[WebSocket]
        self.admin_connections: List[WebSocket] = []

    async def connect_user(self, websocket: WebSocket, user_id: str):
        """Accepts a candidate connection and stores it."""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"✅ Candidate Connected: {user_id}")
        
        # Notify all admins that the user list has changed
        await self.broadcast_to_admins({
            "type": "user-list-update",
            "users": list(self.active_connections.keys())
        })

    async def connect_admin(self, websocket: WebSocket):
        """Accepts an admin connection and sends them the current user list."""
        await websocket.accept()
        self.admin_connections.append(websocket)
        print(f"🛡️ Admin Connected. Total Admins: {len(self.admin_connections)}")
        
        # Send current online users to the new admin immediately
        await websocket.send_json({
            "type": "user-list-update",
            "users": list(self.active_connections.keys())
        })

    def disconnect_user(self, user_id: str):
        """Removes a candidate and notifies admins."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"❌ Candidate Disconnected: {user_id}")

    def disconnect_admin(self, websocket: WebSocket):
        """Removes an admin connection."""
        if websocket in self.admin_connections:
            self.admin_connections.remove(websocket)
            print("❌ Admin Disconnected")

    async def send_message_to_user(self, user_id: str, message: dict):
        """Sends a JSON message to a specific candidate."""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error sending to user {user_id}: {e}")
                self.disconnect_user(user_id)

    async def broadcast_to_admins(self, message: dict):
        """Sends a JSON message to ALL connected admins."""
        # Iterate over a copy to avoid issues if a socket disconnects during loop
        for connection in self.admin_connections.copy():
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to admin: {e}")
                self.disconnect_admin(connection)

# Global instance
socket_manager = ConnectionManager()