
from fastapi import HTTPException

from core import utils
from core.db.uow import UnitOfWork
from database.models.users import UserModel
from database.schemas.users import UserCreateSchema
from database.schemas.users import UserReadSchema


class UserAuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow: UnitOfWork = uow


    async def authenticate_user(self, email: str, password: str) -> UserModel | None:
        async with self.uow as uow:
            user = await uow.users.get_by_email(email)
            
        if not user:
            return None
        if not self.verify_password(password, user.pass_hash):
            return None
        if user.is_deleted:
            return None
        
        return user

    def verify_password(self, password: str, pass_hash: str) -> bool:
        # `pass_hash` may be stored as `str` or `bytes` depending on DB/driver.
        # Ensure we pass `bytes` to `validate_password` and return its result.
        if isinstance(pass_hash, str):
            hashed = pass_hash.encode()
        else:
            hashed = pass_hash

        return utils.validate_password(password, hashed)
    
    
    async def register_user(self, data: UserCreateSchema) -> UserModel:
        async with self.uow as uow:
            user = await uow.users.get_by_email(data.email)
            if user:
                raise HTTPException(status_code=400, detail="Email already registered")

            pass_hash = utils.hash_password(data.password)
            if isinstance(pass_hash, bytes):
                pass_hash = pass_hash.decode()
            
            new_user = await uow.users.create_user(
                username=data.username,
                email=data.email,
                pass_hash=pass_hash
            )
            
            return new_user
    
    async def get_user_by_id(self, user_id: int) -> UserReadSchema | None:
        async with self.uow as uow:
            user = await uow.users.get_by_id(user_id)
            if not user or user.is_deleted:
                return None

            return UserReadSchema.model_validate(user, from_attributes=True)