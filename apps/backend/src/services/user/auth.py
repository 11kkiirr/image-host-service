
from apps.backend.src.core.db.uow import UnitOfWork
from core import utils
from database.repositories.users import UserRepository


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
    
    async def register_user(self, email: str, password: str, username: str) -> bool:
        async with self.uow as uow:
            user = uow.users.get_by_email(email)
            if user:
                return False
            
            pass_hash = utils.hash_password(password)
            new_user = uow.users.create_user(email=email, pass_hash=pass_hash)
            return True