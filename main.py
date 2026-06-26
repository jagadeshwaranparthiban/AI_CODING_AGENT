from fastapi import FastAPI

from db.database import engine
from db.models import Base
from api.routes import router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Code Generation Agent",
    version="0.1.0"
)

# Register API routes
app.include_router(router)


@app.get("/")
def home():
    return {
        "status": "running",
        "service": "Code Generation Agent"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }