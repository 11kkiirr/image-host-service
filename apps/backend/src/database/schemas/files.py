from typing import Optional

from core.db.base import BaseSchema, TimestampReadSchema


class FileReadSchema(TimestampReadSchema):
    id: int
    creator_id: int
    
    filename: str
    content_type: str
    size: int
    storage_path: str

    is_deleted: bool

class FileCreateSchema(BaseSchema):
    creator_id: int
    
    filename: str
    content_type: str
    size: int
    storage_path: str


class FileUpdateSchema(BaseSchema):
    filename: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    storage_path: Optional[str] = None