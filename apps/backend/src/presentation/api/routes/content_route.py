from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile

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
    user_id: int = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    incoming_files = uploaded_files or files or []
    if not incoming_files:
        raise HTTPException(status_code=400, detail="No files provided")

    file_service = FileService(uow)
    await file_service.process_file_upload(
        files=incoming_files,
        user_id=user_id
    )
    return {"message": "Files uploaded successfully."}

@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

@router.get("/{content_uuid}")
async def download_file(
    content_uuid: str,
    uow: UnitOfWork = Depends(get_uow)
):
    ...