from datetime import datetime, timedelta, timezone

import jwt
import bcrypt

from core.config import config


def encode_jwt(
    payload: dict, 
    private_key: str = config.auth_jwt.private_key.read_text(), 
    algorithm: str = config.auth_jwt.algorithm
) -> str:
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded

def decode_jwt(
    token: str | bytes, 
    public_key: str = config.auth_jwt.public_key.read_text(), 
    algorithm: str = config.auth_jwt.algorithm
) -> dict:
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
    

def create_access_token(data: dict, expires_delta: timedelta = timedelta(seconds=1800)) -> str:
    """
    Создает JWT токен с указанными данными и временем жизни.
    
    :param data: Данные для включения в токен (например, идентификатор пользователя).
    :param expires_delta: Время жизни токена в секундах (по умолчанию 30 минут).
    :return: Сгенерированный JWT токен.
    """
    
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + expires_delta
    
    to_encode.update({"exp": expire, "type": "access"})
    
    encopded_jwt = encode_jwt(to_encode)
    
    
    return encopded_jwt
        
def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)) -> str:
    """
    Создает JWT токен обновления с указанными данными и временем жизни.
    
    :param data: Данные для включения в токен (например, идентификатор пользователя).
    :param expires_delta: Время жизни токена в секундах (по умолчанию 7 дней).
    :return: Сгенерированный JWT токен обновления.
    """
    
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + expires_delta
    
    to_encode.update({"exp": expire, "type": "refresh"})
    
    encopded_jwt = encode_jwt(to_encode)
    
    
    return encopded_jwt