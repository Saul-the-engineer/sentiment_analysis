import logging
import os

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

from app.routers import inference_sentiment

# Centralized logging configuration
log_level = logging.DEBUG if os.getenv("ENV") == "development" else logging.INFO
logging.basicConfig(
    format="%(levelname)s - %(asctime)s - %(filename)s - %(message)s",
    level=log_level
)
LOGGER = logging.getLogger("SentimentAnalysisAPI")

def create_app() -> FastAPI:
    """
    Application factory for FastAPI.
    This function creates and returns a new FastAPI application instance.
    """
    app = FastAPI()

    # Status check endpoint
    @app.get("/")
    def status_check():
        """Status check endpoint."""
        return {
            "status": "running",
            "version": "1.0.0",
            "uptime": "API is up and running smoothly."
        }

    # Include the router
    app.include_router(inference_sentiment.router)

    return app

if __name__ == "__main__":
    import uvicorn
    app = create_app()  # Create a FastAPI instance using the factory function
    uvicorn.run(app, host="0.0.0.0", port=8000)
