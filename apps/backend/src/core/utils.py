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