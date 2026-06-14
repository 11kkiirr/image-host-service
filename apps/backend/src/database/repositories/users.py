from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.base.repository import BaseRepository
from database.models.users import UserModel


class UserRepository(BaseRepository[UserModel, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserModel, session)

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        result = await self.session.execute(select(self.model).filter(self.model.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, **kwargs) -> UserModel:
        return await self.create(**kwargs)
