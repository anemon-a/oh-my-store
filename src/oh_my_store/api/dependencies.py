from oh_my_store.services import ClientService
from oh_my_store.database.db import async_session_factory
from oh_my_store.services.unit_of_work import SQLAlchemyUnitOFWork


async def get_client_service() -> ClientService:
    return ClientService(SQLAlchemyUnitOFWork(async_session_factory))
