from pydantic import BaseModel, EmailStr


class OrganizationSchemaBase(BaseModel):
    email: EmailStr
    full_name: str


class OrganizationSchemaCreate(OrganizationSchemaBase):
    pass


class OrganizationSchemaUpdate(BaseModel):
    email: EmailStr
    full_name: str | None = None


class OrganizationSchema(OrganizationSchemaBase):
    id: str

    class Config:
        orm_mode = True
