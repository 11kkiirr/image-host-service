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
    username: Optional[str] = None
    email: Optional[str] = None
    pass_hash: Optional[str] = None
    
    is_banned: Optional[bool] = None
    is_deleted: Optional[bool] = None
    
    is_moderator: Optional[bool] = None
    is_admin: Optional[bool] = None
    
    is_email_confirmed: Optional[bool] = None