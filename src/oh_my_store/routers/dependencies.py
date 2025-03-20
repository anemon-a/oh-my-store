from fastapi import Depends
from oh_my_store.db.db import get_session, AsyncSession
from oh_my_store.services.client_service import ClientService
from oh_my_store.repository.client_repository import ClientRepository


async def get_client_service(session: AsyncSession = Depends(get_session)) -> ClientService:
    return ClientService(ClientRepository(session))
