from fastapi import FastAPI, APIRouter
from api.user_api import router as user_router


# Create FastAPI app
app = FastAPI(
    title="Sensor Reading Backend API",
    description="A FastAPI backend for collecting sensor data from IoT devices",
    version="1.0.0"
)

# Include routers
app.include_router(user_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Sensor Reading Backend API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}