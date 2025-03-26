from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Get environment or use default
cors_origins_env = os.getenv("CORS_ORIGINS", "")

default_origins = ["http://localhost:5173", "http://localhost:3000", "http://frontend"]
allowed_origins = cors_origins_env.split(",") if cors_origins_env else default_origins

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
    return {"status": "1 Fuß"}