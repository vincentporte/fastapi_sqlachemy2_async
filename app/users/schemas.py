from pydantic import BaseModel, EmailStr


class UserSchemaBase(BaseModel):
    email: EmailStr
    full_name: str


class UserSchemaCreate(UserSchemaBase):
    pass


class UserSchema(UserSchemaBase):
    id: str

    class Config:
        orm_mode = True
