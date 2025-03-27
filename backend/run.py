import uvicorn
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Determine environment
app_env = os.getenv("APP_ENV", "development")
is_dev = app_env == "development"
is_docker = os.getenv("DOCKER", "false").lower() == "true"

logger.info(f"Starting with APP_ENV={app_env}, DOCKER={is_docker}")

if __name__ == "__main__":
    # Default configuration
    config = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "reload": is_dev and not is_docker,  # Only use reload in development and not in Docker
    }
    
    logger.info(f"Starting server with config: {config}")
    uvicorn.run(**config)