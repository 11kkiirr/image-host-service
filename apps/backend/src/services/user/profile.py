
from fastapi import HTTPException

from core import utils
from core.db.uow import UnitOfWork
from database.models.users import UserModel
from database.schemas.users import UserProfileReadSchema
from database.schemas.users import UserReadSchema


class UserProfileService:
    def __init__(self, uow: UnitOfWork):
        self.uow: UnitOfWork = uow
    
    async def get_user_profile_by_id(self, user_id: int) -> UserProfileReadSchema | None:
        async with self.uow as uow:
            user = await uow.users.get_by_id(user_id)
            if not user or user.is_deleted:
                return None

            return UserProfileReadSchema.model_validate(user, from_attributes=True)
    
    