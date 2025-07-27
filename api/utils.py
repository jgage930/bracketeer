from pydantic import BaseModel
from typing import Type


def into_pydantic(db_model, into: Type[BaseModel]) -> BaseModel:
    d = {}
    for column in db_model.__table__.columns:
        d[column.name] = getattr(db_model, column.name)

    return into(**d)
