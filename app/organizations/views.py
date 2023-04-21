from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import FormData

from app.organizations.models import Organization as OrganizationModel
from app.organizations.schemas import OrganizationSchemaCreate
from app.services.database import get_db
from app.services.utils import get_errors_dict

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/organizations")


@router.get("/", response_class=HTMLResponse)
async def get_organizations_list(request: Request, db: AsyncSession = Depends(get_db)):
    organizations = await OrganizationModel.get_all(db)
    context = {"request": request, "organizations": organizations}
    return templates.TemplateResponse("organizations/list.html", context)


@router.get("/create/", response_class=HTMLResponse)
async def create_organization_init(request: Request):
    form_data: FormData = await request.form()
    return templates.TemplateResponse("organizations/form.html", {"request": request, "form_data": form_data})


@router.post("/create/", response_class=HTMLResponse)
async def create_organization_submit(request: Request, db: AsyncSession = Depends(get_db)):
    form_data: FormData = await request.form()

    try:
        OrganizationSchemaCreate(**form_data)
        await OrganizationModel.create(db, **form_data)
        return RedirectResponse("/organizations/", status_code=302)

    except ValidationError as e:
        # TODO vincentporte : solve mypy error
        errors = get_errors_dict(e.errors())  # type: ignore
        context = {"request": request, "form_data": form_data, "errors": errors}
        return templates.TemplateResponse("organizations/form.html", context)
