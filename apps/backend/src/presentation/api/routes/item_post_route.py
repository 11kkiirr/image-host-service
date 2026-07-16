from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response

from services.item.post import ItemCreateService
from core.db.uow import UnitOfWork, get_uow
from presentation.api.dependencies.auth import get_current_user
from database.schemas.items import ItemCreateSchema, ItemUpdateSchema

router = APIRouter(prefix="/post", tags=["post"])


@router.post("/create_new")
async def create_item(
    item_data: ItemCreateSchema,
    user_id: int = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    service = ItemCreateService(uow)
    try:
        new_item = service.create_item(item_data, user_id)
        return new_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/update")
async def update_item(
    item_data: ItemUpdateSchema,
    item_uuid: UUID,
    user_id: int = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    service = ItemCreateService(uow)
    try:
        updated_item = service.update_item(item_uuid, item_data, user_id)
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create_link")
async def create_link(
    item_uuid: UUID,
    user_id: int = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    service = ItemCreateService(uow)
    try:
        updated_item = service.create_link(item_uuid, user_id)
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))