from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, Boolean, ForeignKey, Enum as SqlEnum, Uuid

from core.db.base.model import Base, TimestampMixin, BaseModel


class FileModel(Base, TimestampMixin):
    __tablename__ = "files"

    uuid: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    creator_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    item_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("items.id"), nullable=True)
    
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    storage_path: Mapped[str] = mapped_column(String(512), nullable=False)
    
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)