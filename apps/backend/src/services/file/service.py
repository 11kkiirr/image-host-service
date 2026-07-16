import os
from uuid import UUID, uuid4
from aiofiles import open as aio_open

from fastapi import HTTPException, UploadFile

from database.schemas.files import FileReadSchema
from database.models.files import FileModel
from core.db.uow import UnitOfWork


ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

class FileService:
    def __init__(self, uow: UnitOfWork):
        self.uow: UnitOfWork = uow
    
    async def get_file_by_uuid(self, uuid: str):
        async with self.uow as uow:
            ...
    
    async def process_file_upload(
        self,
        files: list[UploadFile],
        user_id: int,
        item_uuid: UUID | None = None
    ):
        async with self.uow as uow:
            file_records = []
            for uploaded_file in files:
                filename = uploaded_file.filename
                file_uuid = str(uuid4())
                content_type = uploaded_file.content_type
                file_ext = os.path.splitext(filename)[1].lower() if filename else ""
                
                if content_type not in ALLOWED_TYPES:
                    continue
                if not filename:
                    filename = f"unnamed_{file_uuid}"

                if uploaded_file.size and uploaded_file.size > MAX_FILE_SIZE:
                    continue
                
                file_data = await uploaded_file.read()
                if len(file_data) > MAX_FILE_SIZE:  # 5 MB limit
                    continue  # Skip files that are too large
                
                file_uuid_value = uuid4()
                file_record = FileModel(
                    uuid=file_uuid_value,
                    creator_id=user_id,
                    filename=filename,
                    content_type=content_type,
                    size=len(file_data),
                    storage_path=f"uploads/{file_uuid_value}{file_ext}",
                    item_uuid=item_uuid,
                )
                async with aio_open(f"uploads/{file_uuid_value}{file_ext}", "wb") as f: # type: ignore
                    await f.write(file_data)
                file_records.append(file_record)
            
            await uow.files.create_files(files=file_records)
        return file_records
    
    async def get_file_metadata_by_uuid(self, uuid: str) -> FileReadSchema:
        async with self.uow as uow:
            file_record = await uow.files.get_file_by_uuid(uuid)
            if not file_record:
                raise HTTPException(status_code=404, detail="File not found")
            return FileReadSchema.model_validate(file_record)