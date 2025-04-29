from fastapi import FastAPI
from oh_my_store.api import client_router, supplier_router
from oh_my_store.api.handlers import (
    phone_number_duplicate_handler,
    supplier_not_found_handler,
    client_not_found_handler,
)
from oh_my_store.exceptions import (
    DuplicatePhoneNumberError,
    SupplierNotFoundError,
    ClientNotFoundError,
)

app = FastAPI()
app.include_router(client_router.router)
app.include_router(supplier_router.router)


app.add_exception_handler(ClientNotFoundError, client_not_found_handler)
app.add_exception_handler(SupplierNotFoundError, supplier_not_found_handler)
app.add_exception_handler(DuplicatePhoneNumberError, phone_number_duplicate_handler)
