from typing import Optional
from uuid import UUID

from sqlalchemy import select
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
    
    async def get_file_by_uuid(self, uuid: str | UUID) -> Optional[FileModel]:
        try:
            normalized_uuid = UUID(uuid) if isinstance(uuid, str) else uuid
        except ValueError:
            return None

        result = await self.session.execute(
            select(FileModel).where(FileModel.uuid == normalized_uuid)
        )
        return result.scalar_one_or_none()
