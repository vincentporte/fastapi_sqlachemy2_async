from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database import get_db
from app.users.models import User as UserModel

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/users")


@router.get("/", response_class=HTMLResponse)
async def get_users_list(request: Request, db: AsyncSession = Depends(get_db)):
    users = await UserModel.get_all(db)
    context = {"request": request, "users": users}
    return templates.TemplateResponse("users/list.html", context)
