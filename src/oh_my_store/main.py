from fastapi import FastAPI
from oh_my_store.routers import client_router

app = FastAPI()
app.include_router(client_router.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
