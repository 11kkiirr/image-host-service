from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.src.database.models.items import ItemModel
from core.db.base.repository import BaseRepository


class ItemRepository(BaseRepository[ItemModel, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(ItemModel, session)

    async def create_item(self, **kwargs) -> ItemModel:
        return await self.create(**kwargs)
