from uuid import UUID

from fastapi import HTTPException, UploadFile

from core.db.uow import UnitOfWork
from database.schemas.items import ItemCreateSchema, ItemUpdateSchema
from database.models.items import ItemModel

class ItemGetService:
    def __init__(self, uow: UnitOfWork):
        self.uow: UnitOfWork = uow
    
    async def get_item_by_uuid(self, item_uuid: UUID) -> ItemModel:
        async with self.uow as uow:
            item_model = await uow.items.get_by_id(item_uuid)
            
            if not item_model:
                raise HTTPException(status_code=404, detail="Item not found")
            return item_model
    
    async def get_item_by_hash(self, link_hash: str) -> ItemModel:
        async with self.uow as uow:
            item_model = await uow.items.get_by_link_hash(link_hash)
            
            if not item_model:
                raise HTTPException(status_code=404, detail="Item not found")
            return item_model
    
    async def get_posts_by_user(self, user_id: int) -> list[ItemModel]:
        async with self.uow as uow:
            item_models = await uow.items.get_by_owner_id(user_id)
            return item_models