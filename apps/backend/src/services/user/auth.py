
from fastapi import HTTPException

from core.db.uow import UnitOfWork
from database.models.users import UserModel
from core import utils
from database.schemas.users import UserCreateSchema


class UserAuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow: UnitOfWork = uow


    async def authenticate_user(self, email: str, password: str) -> bool:
        async with self.uow as uow:
            user = await uow.users.get_by_email(email)
            
        if not user:
            return False
        return self.verify_password(password, user.pass_hash)

    def verify_password(self, password: str, pass_hash: str) -> bool:
        
        utils.validate_password(password, pass_hash.encode())
        
        return password == pass_hash
    
    
    async def register_user(self, data: UserCreateSchema) -> UserModel:
        async with self.uow as uow:
            user = await uow.users.get_by_email(data.email)
            if user:
                raise HTTPException(status_code=400, detail="Email already registered")

            pass_hash = utils.hash_password(data.password)
            
            new_user = await uow.users.create_user(
                username=data.username,
                email=data.email,
                pass_hash=pass_hash
            )
            
            return new_user