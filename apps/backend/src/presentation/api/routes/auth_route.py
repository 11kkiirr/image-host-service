from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response

from core import utils
from core.db.uow import UnitOfWork, get_uow

from database.schemas.users import UserCreateSchema, UserLoginSchema
from services.user.auth import UserAuthService
from presentation.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register_user(
    user_data: UserCreateSchema,
    uow: UnitOfWork = Depends(get_uow),
):
    auth_service = UserAuthService(uow)
    
    user = await auth_service.register_user(user_data)
    
    return {"message": "User registered successfully", "user_id": user.id}

@router.post("/login")
async def login(
    login_data: UserLoginSchema, 
    response: Response, # Добавляем response сюда
    uow: UnitOfWork = Depends(get_uow)
):
    auth_service = UserAuthService(uow)
    user = await auth_service.authenticate_user(login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    
    # Генерируем токен
    token = utils.create_access_token({"sub": str(user.id)}, expires_delta=timedelta(minutes=15))
    
    # Записываем токен в куки
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=900,
        expires=900,
        samesite="lax",
        secure=False,             # Поставь True, когда перейдешь на продакшен с HTTPS
    )
    
    return {"message": "Успешный вход"}