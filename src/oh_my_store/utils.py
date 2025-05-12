from dataclasses import fields, is_dataclass
from typing import Any, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm import Relationship

U = TypeVar("U", bound=BaseModel)


def to_dataclass(obj: Any, class_name: Type[Any]) -> Any:
    dict_obj = {}

    for field in fields(class_name):
        value = getattr(obj, field.name, None)

        if is_dataclass(field.type):
            dict_obj[field.name] = to_dataclass(value, field.type)
        elif isinstance(field.type, list):
            pass
        else:
            dict_obj[field.name] = value

    return class_name(**dict_obj)


def to_orm(obj: Any, orm_class: Type[Any]) -> Any:
    dict_obj = {}

    mapper = inspect(orm_class).mapper
    if mapper is None:
        raise ValueError(f"No mapper found for {orm_class}")

    for column_name, column in mapper.attrs.items():
        value = getattr(obj, column_name, None)

        if isinstance(column, Relationship):
            column_class = column.mapper.class_
            if value:
                dict_obj[column_name] = to_orm(value, column_class)
        elif isinstance(column, list):
            pass
        else:
            dict_obj[column_name] = value

    return orm_class(**dict_obj)


def to_pydantic(obj: Any, pydantic_class: Type[U]) -> U:
    return pydantic_class.model_validate(obj)
