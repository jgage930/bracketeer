from pydantic import BaseModel, ConfigDict
from enum import Enum


class SuspensionType(Enum):
    Fork = "Fork"
    Shock = "Shock"
    Other = "Other"


class SuspensionFieldCreate(BaseModel):
    name: str
    min: int
    max: int
    unit: str


class SuspensionFieldRead(SuspensionFieldCreate):
    id: int
    suspension_id: int

    model_config = ConfigDict(from_attributes=True)


class SuspensionCreate(BaseModel):
    name: str
    type: SuspensionType
    fields: list[SuspensionFieldCreate]


class SuspensionRead(SuspensionCreate):
    id: int
    fields: list[SuspensionFieldRead]

    model_config = ConfigDict(from_attributes=True)
