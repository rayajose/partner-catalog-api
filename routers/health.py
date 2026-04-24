from fastapi import APIRouter
from db import get_connection

router = APIRouter()

@router.get(
    "/health",
    summary="Health check",
    description="Returns the health status of the API and database connection."
)
def health_check():
    try:
        conn = get_connection()
        conn.close()

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "error",
            "database": "unreachable"
        }