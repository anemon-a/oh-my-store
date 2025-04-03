from dataclasses import is_dataclass, fields
from typing import Type, Any


class Mapper[T, U]:

    def from_domain_to_orm(self, domain_obj: T, orm_class: Type[U]) -> U:
        kwargs = {}
        for field in fields(domain_obj):
            value = getattr(domain_obj, field.name)
            orm_field_name = getattr(orm_class, field.name, None)

            if is_dataclass(value):
                orm_field_class = (
                    orm_field_name.mapper.class_ if orm_field_name else None
                )
                kwargs[field.name] = self.from_domain_to_orm(value, orm_field_class)

            # elif isinstance(value, list):
            #     inner_type = get_args(field.type)[0]
            #     if is_dataclass(inner_type):
            #         orm_inner_type = (
            #             get_args(orm_field_name.type)[0] if orm_field_name else None
            #         )
            #         kwargs[field.name] = [cls.to_orm(i, orm_inner_type) for i in value]
            #     else:
            #         kwargs[field.name] = value
            else:
                kwargs[field.name] = value

        return orm_class(**kwargs)

    def from_orm_to_domain(self, orm_obj: U, domain_class: Type[T]) -> T:
        kwargs = {}
        for field in fields(domain_class):
            value = getattr(orm_obj, field.name, None)
            if value is None:
                continue

            if is_dataclass(field.type):
                kwargs[field.name] = self.from_orm_to_domain(value, field.type)
            # elif get_origin(field.type) == list:
            #     inner_type = get_args(field.type)[0]
            #     if is_dataclass(inner_type):
            #         kwargs[field.name] = [cls.to_domain(i, inner_type) for i in value]
            #     else:
            #         kwargs[field.name] = value
            else:
                kwargs[field.name] = value

        return domain_class(**kwargs)
