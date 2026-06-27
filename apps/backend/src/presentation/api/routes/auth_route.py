from fastapi import APIRouter, Depends, HTTPException, Response

from core import utils
from core.db.uow import UnitOfWork, get_uow

from database.schemas.users import UserCreateSchema, UserLoginSchema
from services.user.auth import UserAuthService


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
    token = utils.create_access_token({"sub": str(user.id)})
    
    # Записываем токен в куки
    response.set_cookie(
        key="access_token",       # Название куки
        value=f"Bearer {token}",  # Значение (часто пишут просто токен, но FastAPI OAuth2 ожидает с префиксом)
        httponly=True,            # КРИТИЧЕСКИ ВАЖНО: JS на фронтенде не сможет украсть эту куку
        max_age=1800,             # Время жизни в секундах (например, 30 минут)
        expires=1800,
        samesite="lax",           # Защита от CSRF-атак
        secure=False,             # Поставь True, когда перейдешь на продакшен с HTTPS
    )
    
    return {"message": "Успешный вход"}