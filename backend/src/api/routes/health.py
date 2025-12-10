from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime
from src.core.database import qdrant_client

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Check the health status of the API
    """
    try:
        # Test Qdrant connection
        qdrant_status = "connected"
        try:
            qdrant_client.get_collections()
        except:
            qdrant_status = "disconnected"

        # For now, just return basic health info
        # In a real implementation, you'd also check database connectivity
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "details": {
                "db_status": "connected",  # Placeholder - would check actual DB connection
                "qdrant_status": qdrant_status
            }
        }
    except Exception as e:
        return {
            "status": "unavailable",
            "timestamp": datetime.utcnow().isoformat(),
            "details": {
                "error": str(e)
            }
        }