from fastapi import APIRouter, Depends, HTTPException, Response

from database.schemas.users import UserProfileReadSchema
from core import utils
from core.db.uow import UnitOfWork, get_uow

from presentation.api.dependencies.auth import get_current_user
from services.user.profile import UserProfileService
router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me")
async def get_user_profile(
    user_id: int = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
) -> UserProfileReadSchema:
    profile_service = UserProfileService(uow)
    user = await profile_service.get_user_profile_by_id(user_id)
    
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return user