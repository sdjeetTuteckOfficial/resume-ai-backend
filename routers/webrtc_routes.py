from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.webrtc_service import socket_manager 

router = APIRouter()

# ---------------------------------------------------------
# CANDIDATE ENDPOINT (Candidate -> Admin)
# ---------------------------------------------------------
@router.websocket("/ws/candidate/{user_id}")
async def candidate_endpoint(websocket: WebSocket, user_id: str):
    await socket_manager.connect_user(websocket, user_id)
    try:
        while True:
            # Receive data from the Candidate's frontend
            data = await websocket.receive_json()
            
            # Message Structure expected from Frontend:
            # { "target": "admin", "type": "answer" or "ice-candidate", "payload": { ... } }
            
            target_type = data.get("target")
            
            if target_type == "admin":
                # Forward the candidate's Signal (Answer/ICE) to ALL admins
                # (Or you could track specific admin IDs to be more precise)
                await socket_manager.broadcast_to_admins({
                    "type": "signal",
                    "sender": user_id,
                    "data": data.get("payload") # This contains the SDP or ICE candidate
                })
                
    except WebSocketDisconnect:
        socket_manager.disconnect_user(user_id)
        # Update admins that user left
        await socket_manager.broadcast_to_admins({
            "type": "user-list-update",
            "users": list(socket_manager.active_connections.keys())
        })
    except Exception as e:
        print(f"Error in candidate socket: {e}")
        socket_manager.disconnect_user(user_id)


# ---------------------------------------------------------
# ADMIN ENDPOINT (Admin -> Candidate)
# ---------------------------------------------------------
@router.websocket("/ws/admin")
async def admin_endpoint(websocket: WebSocket):
    await socket_manager.connect_admin(websocket)
    try:
        while True:
            # Receive data from the Admin's frontend
            data = await websocket.receive_json()
            
            # Message Structure expected from Admin Frontend:
            # { "targetUserId": "123", "type": "offer" or "ice-candidate", "payload": { ... } }
            
            target_user_id = data.get("targetUserId")
            
            if target_user_id:
                # Route the Admin's Signal (Offer/ICE) to the specific Candidate
                await socket_manager.send_message_to_user(target_user_id, {
                    "type": "signal",
                    "sender": "admin",
                    "data": data.get("payload") # This contains the SDP or ICE candidate
                })
            else:
                print("⚠️ Admin sent message without targetUserId")

    except WebSocketDisconnect:
        socket_manager.disconnect_admin(websocket)
    except Exception as e:
        print(f"Error in admin socket: {e}")
        socket_manager.disconnect_admin(websocket)