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
use_https = os.getenv("USE_HTTPS", "true").lower() == "true"
is_dev = app_env == "development"

if __name__ == "__main__":
    # Default configuration
    config = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "reload": is_dev,  # Only use reload in development
    }
    
    # Set up HTTPS if enabled
    if use_https:
        # Path to certificates depends on environment
        cert_dir = "../certs/dev" if is_dev else "../certs/prod"
        cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), cert_dir)
        
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