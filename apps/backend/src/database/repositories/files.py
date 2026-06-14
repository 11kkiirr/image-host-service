from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from database.models.files import FileModel
from core.db.base.repository import BaseRepository


class FileRepository(BaseRepository[FileModel, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(FileModel, session)

    async def create_file(self, **kwargs) -> FileModel:
        return await self.create(**kwargs)
