from typing import Optional

from pydantic import Field, EmailStr

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
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)


class UserUpdateSchema(BaseSchema):
    username: Optional[str] = None
    email: Optional[str] = None
    pass_hash: Optional[str] = None
    
    is_banned: Optional[bool] = None
    is_deleted: Optional[bool] = None
    
    is_moderator: Optional[bool] = None
    is_admin: Optional[bool] = None
    
    is_email_confirmed: Optional[bool] = None
    
class UserLoginSchema(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)