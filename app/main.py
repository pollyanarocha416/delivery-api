import os
from typing import cast
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi_pagination import add_pagination
from pathlib import Path
from passlib.context import CryptContext
from dotenv import load_dotenv


env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY não está definida no .env")

SECRET_KEY = cast(str, SECRET_KEY)

ALGORITHM = os.getenv("ALGORITHM")
if not ALGORITHM:
    raise ValueError("ALGORITHM não está definida no .env")

ALGORITHM = cast(str, ALGORITHM)

# parse seguro com fallback para 30 minutos
_raw_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(_raw_minutes) if _raw_minutes not in (None, "") else 30
except (ValueError, TypeError):
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-form")

add_pagination(app)

from app.routes.auth_routes import auth_router
from app.routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)
