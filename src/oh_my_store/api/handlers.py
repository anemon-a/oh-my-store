from fastapi import Request
from fastapi.responses import JSONResponse

from oh_my_store.exceptions import (
    DuplicatePhoneNumberError,
    SupplierNotFoundError,
    ClientNotFoundError,
)


async def client_not_found_handler(
    request: Request, exc: ClientNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def supplier_not_found_handler(
    request: Request, exc: SupplierNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"dateal": str(exc)})


async def phone_number_duplicate_handler(
    request: Request, exc: DuplicatePhoneNumberError
) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})
