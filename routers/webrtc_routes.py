from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# Make sure this import matches your folder structure exactly!
from services.webrtc_service import socket_manager 

router = APIRouter()

# URL: ws://localhost:8000/ws/candidate/{user_id}
@router.websocket("/ws/candidate/{user_id}")
async def candidate_endpoint(websocket: WebSocket, user_id: str):
    await socket_manager.connect_user(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            target_type = data.get("target") 
            
            # Forward signaling data (Offer/Ice Candidate) to Admins
            if target_type == "admin":
                await socket_manager.broadcast_to_admins({
                    "type": "signal",
                    "sender": user_id,
                    "data": data.get("payload")
                })
    except WebSocketDisconnect:
        socket_manager.disconnect_user(user_id)
        await socket_manager.broadcast_to_admins({
            "type": "user-list-update",
            "users": list(socket_manager.active_connections.keys())
        })
    except Exception as e:
        print(f"Error in candidate socket: {e}")

# URL: ws://localhost:8000/ws/admin
@router.websocket("/ws/admin")
async def admin_endpoint(websocket: WebSocket):
    await socket_manager.connect_admin(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            target_user = data.get("targetUserId")
            
            # Forward signaling data (Answer/Ice Candidate/Request) to specific User
            if target_user and target_user in socket_manager.active_connections:
                user_ws = socket_manager.active_connections[target_user]
                await socket_manager.send_personal_message({
                    "type": "signal",
                    "sender": "admin",
                    "data": data.get("payload")
                }, user_ws)
    except WebSocketDisconnect:
        socket_manager.disconnect_admin(websocket)
    except Exception as e:
        print(f"Error in admin socket: {e}")