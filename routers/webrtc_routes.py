from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, status, WebSocketException
from sqlalchemy.orm import Session
from jose import JWTError, jwt

# Import your existing utilities and models
from database import get_db
from config import settings
from models.user import User
from services.webrtc_service import socket_manager 

router = APIRouter()

# --- DEPENDENCY: Validate Token for WebSockets ---
async def get_socket_user(
    websocket: WebSocket,
    token: str = Query(..., description="JWT Token"),
    db: Session = Depends(get_db)
):
    """
    Decodes the JWT token from the query parameter and validates the user.
    If invalid, it closes the socket with a Policy Violation code.
    """
    try:
        # Decode Token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid Token")
            
        # Fetch User from DB
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="User Not Found")
            
        return user

    except JWTError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Could not validate credentials")


# ---------------------------------------------------------
# CANDIDATE ENDPOINT
# URL: ws://localhost:8000/ws/candidate?token=eyJhbG...
# ---------------------------------------------------------
@router.websocket("/ws/candidate")
async def candidate_endpoint(
    websocket: WebSocket, 
    user: User = Depends(get_socket_user)
):
    # Use username as the unique ID for the connection manager
    # (You can also use str(user.id) if you prefer database IDs)
    user_identifier = user.username 

    await socket_manager.connect_user(websocket, user_identifier)
    
    try:
        while True:
            data = await websocket.receive_json()
            target_type = data.get("target")
            
            if target_type == "admin":
                await socket_manager.broadcast_to_admins({
                    "type": "signal",
                    "sender": user_identifier, # Authenticated User ID
                    "data": data.get("payload")
                })
                
    except WebSocketDisconnect:
        socket_manager.disconnect_user(user_identifier)
        await socket_manager.broadcast_to_admins({
            "type": "user-list-update",
            "users": list(socket_manager.active_connections.keys())
        })
    except Exception as e:
        # print(f"Error in candidate socket: {e}")
        socket_manager.disconnect_user(user_identifier)


# ---------------------------------------------------------
# ADMIN ENDPOINT
# URL: ws://localhost:8000/ws/admin?token=eyJhbG...
# ---------------------------------------------------------
@router.websocket("/ws/admin")
async def admin_endpoint(
    websocket: WebSocket, 
    user: User = Depends(get_socket_user)
):
    # Enforce Admin Role Check
    if user.role != "admin": # Ensure your Enum comparison works here, or use user.role.value
        print(f"⚠️ Unauthorized Admin Access Attempt by: {user.email}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await socket_manager.connect_admin(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            target_user_id = data.get("targetUserId")
            
            if target_user_id:
                await socket_manager.send_message_to_user(target_user_id, {
                    "type": "signal",
                    "sender": "admin",
                    "data": data.get("payload")
                })
            else:
                print("⚠️ Admin sent message without targetUserId")

    except WebSocketDisconnect:
        socket_manager.disconnect_admin(websocket)
    except Exception as e:
        # print(f"Error in admin socket: {e}")
        socket_manager.disconnect_admin(websocket)