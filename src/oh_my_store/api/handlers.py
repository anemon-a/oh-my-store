from fastapi import Request
from fastapi.responses import JSONResponse

from oh_my_store.exceptions import (
    ClientNotFoundError,
    DuplicatePhoneNumberError,
    SupplierNotFoundError,
)


async def client_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, ClientNotFoundError):
        raise exc
    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def supplier_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, SupplierNotFoundError):
        raise exc
    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def phone_number_duplicate_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    if not isinstance(exc, DuplicatePhoneNumberError):
        raise exc
    return JSONResponse(status_code=400, content={"detail": str(exc)})
