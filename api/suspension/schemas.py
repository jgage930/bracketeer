from typing_extensions import Self
from pydantic import BaseModel, ConfigDict, model_validator
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

    @model_validator(mode="after")
    def check_min_max(self) -> Self:
        if self.min > self.max:
            raise ValueError("Min valued must be less than the max.")

        return self


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
