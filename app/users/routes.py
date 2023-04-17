from typing import Dict, Mapping

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database import get_db
from app.users.dependencies import valid_user_id
from app.users.models import User as UserModel
from app.users.schemas import UserSchema, UserSchemaCreate, UserSchemaUpdate

router = APIRouter(prefix="/users")


@router.get("/{user_id}/", response_model=UserSchema)
async def get_user(user: Mapping = Depends(valid_user_id)):
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
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return user


@router.patch("/{user_id}/", response_model=UserSchema)
async def update_user(
    user_datas: UserSchemaUpdate, user: UserSchema = Depends(valid_user_id), db: AsyncSession = Depends(get_db)
):
    updated_data = user_datas.dict(exclude_unset=True)
    user = await UserModel.update(db, user, **updated_data)
    if not user:
        raise HTTPException(status_code=400, detail="Email already exists")
    return user


@router.delete("/{user_id}/", response_model=Dict[str, str])
async def delete_user(user: dict = Depends(valid_user_id), db: AsyncSession = Depends(get_db)):
    res = await UserModel.delete(user, db)
    return {"message": f"User {res} deleted successfully"}
