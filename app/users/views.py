from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import FormData

from app.services.database import get_db
from app.services.utils import get_errors_dict
from app.users.models import User as UserModel
from app.users.schemas import UserSchemaCreate

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/users")


@router.get("/", response_class=HTMLResponse)
async def get_users_list(request: Request, db: AsyncSession = Depends(get_db)):
    users = await UserModel.get_all(db)
    context = {"request": request, "users": users}
    return templates.TemplateResponse("users/list.html", context)


@router.get("/create/", response_class=HTMLResponse)
async def create_user_init(request: Request):
    form_data: FormData = await request.form()
    return templates.TemplateResponse("users/form.html", {"request": request, "form_data": form_data})


@router.post("/create/", response_class=HTMLResponse)
async def create_user_submit(request: Request, db: AsyncSession = Depends(get_db)):
    form_data: FormData = await request.form()

    try:
        UserSchemaCreate(**form_data)
        await UserModel.create(db, **form_data)
        return RedirectResponse("/users/", status_code=302)

    except ValidationError as e:
        # TODO vincentporte : solve mypy error
        errors = get_errors_dict(e.errors())  # type: ignore
        context = {"request": request, "form_data": form_data, "errors": errors}
        return templates.TemplateResponse("users/form.html", context)
