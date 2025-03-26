from dataclasses import dataclass


@dataclass
class Address:
    country: str
    city: str
    street: str

    def check_existing() -> bool:
        pass
