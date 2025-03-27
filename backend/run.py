import uvicorn
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Determine environment and HTTPS settings
app_env = os.getenv("APP_ENV", "development")
is_dev = app_env == "development"
is_docker = os.getenv("DOCKER", "false").lower() == "true"
is_server = not is_dev  # If not dev, assume server/production

# Only use HTTPS on server, not for any local development
use_https = is_server and os.getenv("USE_HTTPS", "true").lower() == "true"

logger.info(f"Starting with APP_ENV={app_env}, USE_HTTPS={use_https}, DOCKER={is_docker}")

if __name__ == "__main__":
    # Default configuration - use HTTP for all local development
    config = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "reload": is_dev and not is_docker,  # Only use reload in development and not in Docker
    }
    
    # Only use HTTPS in server environment
    if use_https and is_server:
        cert_path = "/app/certs/prod"
        
        ssl_keyfile = os.path.join(cert_path, "key.pem")
        ssl_certfile = os.path.join(cert_path, "cert.pem")
        
        if os.path.exists(ssl_keyfile) and os.path.exists(ssl_certfile):
            config["ssl_keyfile"] = ssl_keyfile
            config["ssl_certfile"] = ssl_certfile
            # Update port for HTTPS
            config["port"] = 8443
            logger.info(f"HTTPS enabled in {app_env} environment on port {config['port']}")
        else:
            logger.warning(f"HTTPS requested but certificates not found in {cert_path}")
            logger.warning("Falling back to HTTP")
    
    logger.info(f"Starting server with config: {config}")
    uvicorn.run(**config)