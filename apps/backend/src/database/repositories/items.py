from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.src.database.models.items import Item
from core.db.base.repository import BaseRepository


class ItemRepository(BaseRepository[Item, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(Item, session)

    async def create_item(self, **kwargs) -> Item:
        return await self.create(**kwargs)
