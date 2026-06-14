from typing import Optional

from core.db.base import BaseSchema, TimestampReadSchema


class UserReadSchema(TimestampReadSchema):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    pass_hash: str
    
    is_banned: bool
    is_deleted: bool
    
    is_moderator: bool
    is_admin: bool
    
    is_email_confirmed: bool


class UserCreateSchema(BaseSchema):
    username: Optional[str] = None
    email: Optional[str] = None
    pass_hash: str


class UserUpdateSchema(BaseSchema):
    username: Optional[str] = None
    email: Optional[str] = None
    pass_hash: Optional[str] = None
    
    is_banned: Optional[bool] = None
    is_deleted: Optional[bool] = None
    
    is_moderator: Optional[bool] = None
    is_admin: Optional[bool] = None
    
    is_email_confirmed: Optional[bool] = None