from pydantic import BaseModel


class UserSchemaBase(BaseModel):
    # todo : convert to email type
    email: str | None = None
    full_name: str | None = None


class UserSchemaCreate(UserSchemaBase):
    pass


class UserSchema(UserSchemaBase):
    id: str

    class Config:
        orm_mode = True
