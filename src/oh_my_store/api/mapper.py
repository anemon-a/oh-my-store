from dataclasses import fields, is_dataclass
from typing import Type


class Mapper[T, U]:
    @staticmethod
    def from_pydantic_to_domain(pydantic_obj: T, domain_class: Type[U]) -> U:
        kwargs = {}

        for field in fields(domain_class):
            value = getattr(pydantic_obj, field.name, None)

            if value is None:
                continue

            if is_dataclass(field.type):
                kwargs[field.name] = Mapper.from_pydantic_to_domain(value, field.type)

            else:
                kwargs[field.name] = value

        return domain_class(**kwargs)

    def from_domain_to_pydantic(self) -> T:
        pass
