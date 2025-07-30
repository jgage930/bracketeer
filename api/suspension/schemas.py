from pydantic import BaseModel
from enum import Enum


class SuspensionType(Enum):
    Fork = "Fork"
    Shock = "Shock"
    Other = "Other"


class SuspensionFieldCreate(BaseModel):
    min: int
    max: int
    unit: str


class SuspensionFieldRead(BaseModel):
    id: int
    suspension_id: int


class SuspensionCreate(BaseModel):
    name: str
    type: SuspensionType
    fields: list[SuspensionFieldCreate]


class SuspensionRead(BaseModel):
    id: int
