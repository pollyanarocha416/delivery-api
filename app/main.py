import os
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from pathlib import Path
from passlib.context import CryptContext
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


from app.routes.auth_routes import auth_router
from app.routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)
