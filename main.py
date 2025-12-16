# ==================== main.py ====================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

# --- Router Imports ---
from routers import auth
from routers.job_router import router as job_router
from routers.user_details_entry import router as user_details_entry_router
from routers.interview_routes import router as interview_details_router
from routers.webrtc_routes import router as webrtc_routes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI backend API documentation for ResumeAI")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(job_router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(user_details_entry_router, prefix="/api/user_details", tags=["User Details"])
app.include_router(interview_details_router, prefix="/api/gap", tags=["Gap analysis"])

# --- WebRTC Router (No Prefix) ---
# This ensures the URL is exactly: ws://localhost:8000/ws/candidate/...
app.include_router(webrtc_routes, tags=["WebRTC unprotected test"])

@app.get("/")
def read_root():
    return {"message": "FastAPI Auth System API"}

# --- DEBUG: Print Routes on Startup ---
# This script will run every time you start the server to prove the routes exist
@app.on_event("startup")
async def startup_event():
    print("\n=====================================")
    print("🚀 SERVER STARTED. CHECKING ROUTES:")
    print("=====================================")
    found_ws = False
    for route in app.routes:
        # Check for WebSocket routes
        if hasattr(route, "path") and "/ws/" in route.path:
            print(f"✅ ACTIVE WEBSOCKET: {route.path}")
            found_ws = True
    
    if not found_ws:
        print("❌ CRITICAL: No WebSocket routes found! Check routers/webrtc_routes.py")
    print("=====================================\n")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)