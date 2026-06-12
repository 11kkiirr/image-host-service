from typing import Optional

from core.db.base import BaseSchema, TimestampReadSchema


class FileRead(TimestampReadSchema):
    id: int
    creator_id: int
    
    filename: str
    content_type: str
    size: int
    storage_path: str

    is_deleted: bool

class FileCreate(BaseSchema):
    creator_id: int
    
    filename: str
    content_type: str
    size: int
    storage_path: str


class FileUpdate(BaseSchema):
    filename: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    storage_path: Optional[str] = None