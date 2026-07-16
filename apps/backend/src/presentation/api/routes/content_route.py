from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

from database.schemas.users import UserProfileReadSchema
from core import utils
from core.db.uow import UnitOfWork, get_uow

from presentation.api.dependencies.auth import get_current_user
from services.file.service import FileService


router = APIRouter(prefix="/file", tags=["file"])


@router.post("/upload")
async def upload_multiple_files(
    files: Annotated[list[UploadFile] | None, File(alias="files")] = None,
    uploaded_files: Annotated[list[UploadFile] | None, File(alias="uploaded_files")] = None,
    item_uuid: UUID | None = None,
    user_id: int = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    incoming_files = uploaded_files or files or []
    if not incoming_files:
        raise HTTPException(status_code=400, detail="No files provided")

    file_service = FileService(uow)
    
    file_records = await file_service.process_file_upload(
        files=incoming_files,
        user_id=user_id,
        item_uuid=item_uuid
    )
    return {
        "message": "Files uploaded successfully.",
        "files": file_records
    }

@router.get("/{content_uuid}")
async def download_file(
    content_uuid: str,
    uow: UnitOfWork = Depends(get_uow)
):
    file_service = FileService(uow)
    
    file_metadata = await file_service.get_file_metadata_by_uuid(content_uuid)
    return FileResponse(path=file_metadata.storage_path, filename=f"{file_metadata.filename}")