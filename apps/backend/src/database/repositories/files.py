from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from database.models.files import FileModel
from core.db.base.repository import BaseRepository


class FileRepository(BaseRepository[FileModel, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(FileModel, session)

    async def create_files(self, files: list[FileModel]) -> list[FileModel]:
        self.session.add_all(files)
        await self.session.flush()
        for file in files:
            await self.session.refresh(file)
        return files
    
    async def get_file_by_uuid(self, uuid: str) -> Optional[FileModel]:
        result = await self.session.execute(
            self.model.__table__.select().where(self.model.uuid == uuid)
        )
        return result.scalar_one_or_none()
