from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database import get_db
from app.users.models import User as UserModel
from app.users.schemas import UserSchema, UserSchemaCreate

router = APIRouter(prefix="/users")


@router.get("/{id}/", response_model=UserSchema)
async def get_user(id: str, db: AsyncSession = Depends(get_db)):
    user = await UserModel.get(db, id)
    return user


# todo : add pagination
# todo : add authentification
@router.get("/", response_model=list[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await UserModel.get_all(db)
    return users


@router.post("/create/", response_model=UserSchema)
async def create_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_db)):
    user = await UserModel.create(db, **user.dict())
    return user
