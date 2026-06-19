from fastapi import APIRouter, Depends

from core import utils
from core.db.uow import get_uow

from database.schemas.users import UserCreateSchema
from services.user.auth import UserAuthService


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register_user(
    user_data: UserCreateSchema,
    uow=Depends(get_uow),
):
    auth_service = UserAuthService(uow)
    
    user = await auth_service.register_user(user_data)
    
    return {"message": "User registered successfully", "user_id": user.id}