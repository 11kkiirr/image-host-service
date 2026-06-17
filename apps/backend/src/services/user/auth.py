
from core import utils
from database.repositories.users import UserRepository


class UserAuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository: UserRepository = user_repository


    def authenticate_user(self, email: str, password: str) -> bool:
        async with uow as uow:
            user = self.user_repository.get_by_email(email)
            
        if not user:
            return False
        return self.verify_password(password, user.pass_hash)

    def verify_password(self, password: str, pass_hash: str) -> bool:
        # Implement password verification logic here (e.g., using bcrypt)
        return password == pass_hash  # Placeholder for demonstration