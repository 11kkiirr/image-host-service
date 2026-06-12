from typing import Optional

from core.db.base import BaseSchema, TimestampReadSchema


class ItemRead(TimestampReadSchema):
    id: int
    owner_id: int
    link_hash: str
    
    title: str
    description: Optional[str] = None
    file_id: int
    
    is_global: bool
    views: int
    likes: int
    
    deleted_at: Optional[str] = None


class ItemCreate(BaseSchema):
    owner_id: int
    link_hash: str
    
    title: str
    description: Optional[str] = None
    file_id: int
    
    is_global: bool = False


class ItemUpdate(BaseSchema):
    link_hash: Optional[str] = None
    
    title: Optional[str] = None
    description: Optional[str] = None
    file_id: Optional[int] = None
    
    is_global: Optional[bool] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    
    deleted_at: Optional[str] = None