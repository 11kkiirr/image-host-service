# src/presentation/api/deps.py
from fastapi import Request, Depends, HTTPException, status
import jwt
from core.config import config
from core import utils


def get_token_from_cookie(request: Request) -> str:
    """Достаем токен из куки и очищаем от префикса 'Bearer '"""
    token_with_prefix = request.cookies.get("access_token")
    if not token_with_prefix:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Вы не авторизованы (кука отсутствует)"
        )
    
    # Если ты записывал куку как "Bearer <token>"
    if token_with_prefix.startswith("Bearer "):
        return token_with_prefix.split(" ")[1]
    
    return token_with_prefix

async def get_current_user(
    token: str = Depends(get_token_from_cookie),
):
    try:
        payload = utils.decode_jwt(token)
        user_id = payload.get("sub")
        if not isinstance(user_id, str):
            raise HTTPException(status_code=401, detail="Невалидный токен")
        return int(user_id)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Токен истек или изменен")