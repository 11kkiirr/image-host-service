from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response

from apps.backend.src.services.item.get import ItemGetService
from services.item.post import ItemCreateService
from core.db.uow import UnitOfWork, get_uow
from presentation.api.dependencies.auth import get_current_user
from database.schemas.items import ItemCreateSchema, ItemUpdateSchema

router = APIRouter(prefix="/p", tags=["post_get"])


@router.get("/u/{item_uuid}")
async def get_item(
    item_uuid: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    service = ItemGetService(uow)
    try:
        item_model = await service.get_item_by_uuid(item_uuid)
        return item_model
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/h/{link_hash}")
async def get_item_by_hash(
    link_hash: str,
    uow: UnitOfWork = Depends(get_uow)
):
    service = ItemGetService(uow)
    try:
        item_model = await service.get_item_by_hash(link_hash)
        return item_model
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my_posts")
async def get_my_posts(
    user_id: int = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    service = ItemGetService(uow)
    try:
        item_models = await service.get_posts_by_user(user_id)
        return item_models
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))