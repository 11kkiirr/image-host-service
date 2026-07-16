from typing import Optional
from uuid import UUID

from core.db.base import BaseSchema, TimestampReadSchema


class ItemReadSchema(TimestampReadSchema):
    uuid: UUID
    owner_id: int
    link_hash: str
    
    title: str | None = None
    description: Optional[str] = None
    
    is_global: bool
    views: int
    likes: int
    
    deleted_at: Optional[str] = None


class ItemCreateSchema(BaseSchema):
    owner_id: int
    link_hash: str | None = None
    
    title: str | None = None
    description: Optional[str] = None
    
    is_global: bool = False


class ItemUpdateSchema(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    
    is_global: Optional[bool] = None