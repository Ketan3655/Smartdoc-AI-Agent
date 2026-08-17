from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.routes import router
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
# Import models so SQLAlchemy creates tables
import app.db.models

app = FastAPI(
    title="SmartDoc AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://smartdoc-ai-agent.vercel.app",
    ],
    allow_origin_regex=r"https://smartdoc-ai-agent-[a-z0-9]+-ketan3655s-projects\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create database tables
Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "SmartDoc AI Running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }