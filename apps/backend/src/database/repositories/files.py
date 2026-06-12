from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from database.models.files import File
from core.db.base.repository import BaseRepository


class FileRepository(BaseRepository[File, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(File, session)

    async def create_file(self, **kwargs) -> File:
        return await self.create(**kwargs)
