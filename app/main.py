from fastapi import FastAPI

app = FastAPI()

from app.routes.auth_routes import auth_router
from app.routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)
