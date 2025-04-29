from uuid import UUID


class ClientNotFoundError(Exception):
    def __init__(self, **kwargs):
        fields = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        super().__init__(f"Client with {fields} not found")


class SupplierNotFoundError(Exception):
    def __init__(self, supplier_id: UUID):
        self.supplier_id = supplier_id
        super().__init__(f"Supplier with id {supplier_id} not found")


class DuplicatePhoneNumberError(Exception):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number
        super().__init__(f"Phone number {phone_number} already exists")
