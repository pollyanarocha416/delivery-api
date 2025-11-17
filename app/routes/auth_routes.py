import traceback
import logging
from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.logging_config import setup_logging
from app.dependencies import pegar_sessao, verify_jwt_token
from app.main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.auth_schemas import UserSchema
from app.schemas.auth_schemas import LoginSchema
from app.db.models import Usuario


setup_logging()
logger = logging.getLogger("my_app")


auth_router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(id_usuario, token_duration=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))):
    try:
        expiration_data = datetime.now(timezone.utc) + token_duration
        dic_info = { "sub": str(id_usuario), "exp": expiration_data }
        encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
        
        logger.info(f"Token created for user {id_usuario} | Expires at {expiration_data.isoformat()}")    
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation error: {traceback.format_exception(type(e), e, e.__traceback__)}")
        raise e

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
                            "email": [
                                "field required", 
                                "value is not a valid email"
                            ],
                            "senha": [
                                "ensure this value has at least 8 characters"
                            ],
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
    try:
        usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
        
        if not usuario:
            raise HTTPException(status_code=404, detail="User not found or incorrect password.")
        else:
            access_token = criar_token(usuario.id)
            refresh_token = criar_token(usuario.id, token_duration=timedelta(days=7))
            
            logger.info(f"POST login {login_schema.email} | 200 OK ")
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
    except JWTError as jwt_error:
        logger.error(f"POST login {login_schema.email} | 401 Unauthorized | {traceback.format_exception(type(jwt_error), jwt_error, jwt_error.__traceback__)}")
        raise HTTPException(status_code=401, detail="Token generation error.")
    except Exception as e:
        logger.error(f"POST login {login_schema.email} | 500 ERRO | {traceback.format_exception(type(e), e, e.__traceback__)}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@auth_router.get(
    path="/refresh",
    summary="Refresh access token",
    description="Generate a new access token using a refresh token",
    status_code=200,
    response_model=dict,
)
async def refresh_token(user: Usuario=Depends(verify_jwt_token)):
    try:
        
        new_access_token = criar_token(user.id)
        new_refresh_token = criar_token(user.id, token_duration=timedelta(days=7))
        logger.info(f"POST refresh token for user {user.id} | 200 OK")

        return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }
        
    except JWTError:
        logger.error(f"POST refresh token | 401 Unauthorized | Invalid refresh token")
        raise HTTPException(status_code=401, detail="Invalid refresh token.")
    except Exception as e:
        logger.error(f"POST refresh token | 500 ERRO | {traceback.format_exception(type(e), e, e.__traceback__)}")
        raise HTTPException(status_code=500, detail="Internal server error.")

