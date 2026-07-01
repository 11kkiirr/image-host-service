from typing import Optional

from pydantic import Field, EmailStr

from core.db.base import BaseSchema, TimestampReadSchema


class UserReadSchema(TimestampReadSchema):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    pass_hash: str | None = None
    
    is_banned: bool | None = None
    is_deleted: bool | None = None
    
    is_moderator: bool | None = None
    is_admin: bool | None = None
    
    is_email_confirmed: bool | None = None


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

class UserProfileReadSchema(BaseSchema):
    id: int
    username: Optional[str] = None
    
    email: Optional[str] = None
    is_email_confirmed: bool | None = None
    
    is_banned: bool | None = None
    
    is_moderator: bool | None = None
    is_admin: bool | None = None