import traceback
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.logging_config import setup_logging
from app.dependencies import pegar_sessao
from app.main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.auth_schemas import UserSchema
from app.schemas.auth_schemas import LoginSchema
from app.db.models import Usuario


setup_logging()
logger = logging.getLogger("my_app")


auth_router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(id_usuario):
    expiration_data = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    dic_info = { "sub": id_usuario, "exp": expiration_data }
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def autenticar_usuario(email: str, senha: str, session: Session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    
    
    return usuario


@auth_router.get(
    path="/",
    description="test",
    status_code=200,
    response_model=dict,
    responses={
        200: {
            "description": "Test",
            "content": {
                "application/json": {
                    "example": {
                        "message": "xxxx"
                    }
                }
            },
        }
    }
)
async def home():
    logger.info("GET auth home | 200 OK")
    return {"message": "test"}


@auth_router.post(
    path="/user", 
    summary="Create new user account",
    description="Create user account with email and password",
    status_code=201,
    response_model=dict,
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User created successfully", 
                        "id": 1, 
                        "email": "user@example.com"
                    }
                }
            },
        },
        400: {
            "description": "user already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "user already exists"
                    }
                }
            },
        },
        422: {
            "description": "invalid input data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "email": ["field required", "value is not a valid email"],
                            "senha": ["ensure this value has at least 8 characters"],
                        }
                    }
                }
            },
        }
    }
)
async def user(user: UserSchema, session: Session=Depends(pegar_sessao)):
    try:
        usuario = session.query(Usuario).filter_by(email=user.email).first()

        if usuario:
            raise HTTPException(status_code=400, detail="User already exists.")
        else:
            senha_criptografada = bcrypt_context.hash(user.senha)
            
            new_user = Usuario(user.nome, user.email, senha_criptografada, user.ativo, user.admin)
            ativo = user.ativo if user.ativo is not None else True
            admin = user.admin if user.admin is not None else False
            new_user = Usuario(user.nome, user.email, senha_criptografada, ativo, admin)

            session.add(new_user)
            session.commit()
            logger.info(f"POST user {user.email} | 200 OK")
            return {"mensagem": f"User created successfully {user.email}"}
    except Exception as e:
        logger.error(f"POST user {user.email} | 500 ERRO | {traceback.format_exception(type(e), e, e.__traceback__)}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error.")


@auth_router.post(
    path="/login",
    summary="Login user and generate token",
    description="Authenticate user and return access token",
    status_code=200,
    response_model=dict,
)
async def login(login_schema: LoginSchema, session: Session=Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="User not found or incorrect password.")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token, "token_type": "bearer"}
