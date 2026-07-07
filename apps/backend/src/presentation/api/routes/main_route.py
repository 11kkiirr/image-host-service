import os
from typing import List

from fastapi import APIRouter, UploadFile, UploadFile
from fastapi.responses import FileResponse, HTMLResponse


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_index():
    # Возвращаем наш HTML файл как ответ на GET "/"
    return FileResponse(os.path.join("static", "index.html"))