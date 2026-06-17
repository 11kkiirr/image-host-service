from fastapi import APIRouter, Depends

from core import utils
from database.schemas.users import UserCreateSchema

router = APIRouter(prefix="/auth", tags=["auth"])


def validate_registration_data():
    ...

router.post("/register")
async def register_user(
    user: UserCreateSchema = Depends(validate_registration_data),
):
    ...