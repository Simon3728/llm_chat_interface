from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Get environment or use default
cors_origins_env = os.getenv("CORS_ORIGINS", "")

default_origins = ["http://localhost:5173", "http://localhost:3000", "http://frontend"]
allowed_origins = cors_origins_env.split(",") if cors_origins_env else default_origins

logger.info(f"Configuring CORS with origins: {allowed_origins}")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/health")
async def health_check():
    try:
        # Here you could add a DB connection check if needed
        return {"status": "OK"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Server error")