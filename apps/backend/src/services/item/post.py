from uuid import UUID, uuid4

from fastapi import HTTPException

from core.utils import generate_link_hash
from core.db.uow import UnitOfWork
from database.schemas.items import ItemCreateSchema, ItemUpdateSchema
from database.models.items import ItemModel


class ItemCreateService:
    def __init__(self, uow: UnitOfWork):
        self.uow: UnitOfWork = uow
    
    async def create_item(self, item_data: ItemCreateSchema, user_id: int) -> ItemModel:
        async with self.uow as uow:
            
            item_model = await uow.items.create_item(
                uuid=uuid4(),
                owner_id=user_id,
                title=item_data.title,
                description=item_data.description,
                is_global=item_data.is_global,
            )
            
            return item_model
    
    async def update_item(self, item_uuid: UUID, item_data: ItemUpdateSchema, user_id: int) -> ItemModel:
        async with self.uow as uow:
            item_model = await uow.items.get_by_id(item_uuid)
            
            if not item_model:
                raise HTTPException(status_code=404, detail="Item not found")
            
            if item_model.owner_id != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to update this item")
            
            updated_item = await uow.items.update(
                item_model,
                title=item_data.title,
                description=item_data.description,
                is_global=item_data.is_global,
            )
            
            return updated_item
    
    async def create_link(self, item_uuid: UUID, user_id: int) -> ItemModel:
        async with self.uow as uow:
            item_model = await uow.items.get_by_id(item_uuid)
            
            if not item_model:
                raise HTTPException(status_code=404, detail="Item not found")
            
            if item_model.owner_id != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to create a link for this item")
            
            link_hash = generate_link_hash()
            
            updated_item = await uow.items.update(
                item_model,
                link_hash=link_hash
            )
            
            return updated_item