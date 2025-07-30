from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    access_level_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class AccessLevelCreate(BaseModel):
    name: str


class AccessLevelRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
