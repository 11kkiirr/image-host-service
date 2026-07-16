from typing import Optional
from uuid import UUID

from core.db.base import BaseSchema, TimestampReadSchema


class FileReadSchema(TimestampReadSchema):
    uuid: UUID
    creator_id: int
    item_id: UUID | None = None

    filename: str
    content_type: str
    size: int
    storage_path: str

    is_deleted: bool | None = False

class FileCreateSchema(BaseSchema):
    creator_id: int
    item_id: UUID | None = None
    
    filename: str
    content_type: str
    size: int
    storage_path: str


class FileUpdateSchema(BaseSchema):
    filename: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    storage_path: Optional[str] = None