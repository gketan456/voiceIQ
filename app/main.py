from fastapi import FastAPI
from app.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="VoiceIQ",
    version="1.0.0",
)

@app.get("/health")
def health():
    logger.info("Health check called")
    return {"status": "ok", "app": "VoiceIQ"}

