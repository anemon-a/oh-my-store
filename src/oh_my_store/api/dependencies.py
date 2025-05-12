from oh_my_store.database.db import async_session_factory
from oh_my_store.services.unit_of_work import SQLAlchemyUnitOFWork


async def get_unit_of_work() -> SQLAlchemyUnitOFWork:
    return SQLAlchemyUnitOFWork(async_session_factory)
