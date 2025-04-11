from typing import Type
from dataclasses import is_dataclass, fields
from sqlalchemy import inspect
from sqlalchemy.orm import Relationship


def to_dataclass[T, U](obj: T, class_name: Type[U]) -> U:
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


def to_orm[T, U](obj: T, orm_class: Type[U]) -> U:
    dict_obj = {}

    for column_name, column in inspect(orm_class).mapper.attrs.items():
        value = getattr(obj, column_name, None)

        if isinstance(column, Relationship):
            column_class = column.mapper.class_
            # print(value, type(value), column_class)
            dict_obj[column_name] = to_orm(value, column_class)

        elif isinstance(column, list):
            pass
        else:
            dict_obj[column_name] = value

    return orm_class(**dict_obj)


def to_pydantic[T, U](obj: T, pydantic_class: Type[U]) -> U:
    return pydantic_class.model_validate(obj)
