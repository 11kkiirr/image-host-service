from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from database.models.items import ItemModel
from core.db.base.repository import BaseRepository


class ItemRepository(BaseRepository[ItemModel, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(ItemModel, session)

    async def get_by_id(self, item_uuid: UUID) -> ItemModel | None:
        return await self.get(item_uuid)
    
    async def get_by_link_hash(self, link_hash: str) -> ItemModel | None:
        result = await self.get_by_criteria(link_hash=link_hash)
        return result
    
    async def get_by_owner_id(self, owner_id: int) -> list[ItemModel]:
        return await self.get_all_by_criteria(owner_id=owner_id) # type: ignore
    
    async def create_item(self, **kwargs) -> ItemModel:
        return await self.create(**kwargs)
    
    async def update(self, item: ItemModel, **kwargs) -> ItemModel:
        for key, value in kwargs.items():
            setattr(item, key, value)
        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)
        return item
