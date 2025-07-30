from pydantic import BaseModel
from typing import Type


def into_pydantic(db_model, into: Type[BaseModel]) -> BaseModel:
    d = {}
    for column in db_model.__table__.columns:
        d[column.name] = getattr(db_model, column.name)

    return into(**d)


def into_pydantic_many(db_models, into: Type[BaseModel]) -> list[BaseModel]:
    return [into_pydantic(row, into) for row in db_models]
