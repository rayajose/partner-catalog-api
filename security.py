from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from settings import Settings, get_settings

api_key_header = APIKeyHeader(
    name="X-API-Key",
    scheme_name="APIKeyAuth",
    description="API key required to access this API."
)

def require_api_key(
    api_key: str = Depends(api_key_header),
    settings: Settings = Depends(get_settings),
) -> str:
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key"
        )
    return api_key