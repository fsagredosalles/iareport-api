# Vacío o con medidas básicas:
from fastapi import HDepends, HTTPException, status, Request
from jose import JWTError, jwt
from pydantic import BaseModel


SECRET_KEY = "your-secret-key"  # Genera una clave segura
ALGORITHM = "HS256"

class TokenData(BaseModel):
    username: str | None = None

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

async def get_current_user(token: str = Depends()):
    username = verify_token(token)
    return username

async def validate_request(request: Request):
    """Placeholder para futuras validaciones (ej: CORS)"""
    pass