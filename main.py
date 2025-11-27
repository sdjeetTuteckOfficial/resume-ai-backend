# ==================== main.py ====================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth
from routers.job_router import router as job_router
from routers.user_details_entry import router as user_details_entry_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI backend API documentation for ResumeAI")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(job_router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(user_details_entry_router, prefix="/api/user_details", tags=["User Details"])

@app.get("/")
def read_root():
    return {"message": "FastAPI Auth System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)













