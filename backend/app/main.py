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

# Get CORS origins from environment or use defaults
cors_origins_env = os.getenv("CORS_ORIGINS", "")

# Default origins include both HTTP and HTTPS variants for development
default_origins = [
    # Local development (direct run)
    "http://localhost:5173",
    # Docker HTTP
    "http://localhost:3000",
    # Docker HTTPS
    "https://localhost:3443"
]

# If in production, add server-specific origins
if not IS_DEV:
    server_ip = os.getenv("SERVER_IP", "192.168.0.166")  # Default to your server IP
    default_origins.extend([
        f"http://{server_ip}:3000", f"https://{server_ip}:3000",
        f"http://{server_ip}:3443", f"https://{server_ip}:3443"
    ])

allowed_origins = cors_origins_env.split(",") if cors_origins_env else default_origins

logger.info(f"Running in {ENV} environment")
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
    return {"message": "Hello World", "environment": ENV}

@app.get("/api/health")
async def health_check():
    try:
        # Here you could add a DB connection check if needed
        return {"status": "OK", "environment": ENV}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Server error")