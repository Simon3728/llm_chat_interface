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

# Determine environment
ENV = os.getenv("APP_ENV", "development")
IS_DEV = ENV == "development"
IS_DOCKER = os.getenv("DOCKER", "false").lower() == "true"
USE_HTTPS = os.getenv("USE_HTTPS", "false").lower() == "true" or IS_DOCKER

# Get CORS origins from environment or use defaults
cors_origins_env = os.getenv("CORS_ORIGINS", "")

# Default origins set based on environment
if IS_DEV and not IS_DOCKER:
    # Local development without Docker - HTTPs
    default_origins = ["http://localhost:5173"]
elif IS_DOCKER:
    # Docker environment - HTTPS by default
    default_origins = ["http://localhost:3000"]
else:
    # Production (server) - will be determined later
    default_origins = []
    server_ip = os.getenv("SERVER_IP", "192.168.0.166")
    default_origins.extend([
        f"https://{server_ip}:3443",
        "https://yourdomain.com"  # Replace with your actual domain
    ])

# If explicit CORS settings provided, use those
allowed_origins = cors_origins_env.split(",") if cors_origins_env else default_origins

logger.info(f"Running in {ENV} environment with Docker={IS_DOCKER}, HTTPS={USE_HTTPS}")
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
    return {
        "message": "Hello World", 
        "environment": ENV,
        "docker": IS_DOCKER,
        "https": USE_HTTPS,
        "cors_origins": allowed_origins
    }

@app.get("/api/health")
async def health_check():
    try:
        # Here you could add a DB connection check if needed
        return {
            "status": "OK", 
            "environment": ENV,
            "docker": IS_DOCKER
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Server error")