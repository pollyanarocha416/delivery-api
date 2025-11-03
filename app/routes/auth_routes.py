import traceback
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import pegar_sessao
from app.main import bcrypt_context
from app.schemas.auth_schemas import UsuarioSchema
from app.schemas.auth_schemas import LoginSchema
from app.db.models import Usuario
from app.logging_config import setup_logging


setup_logging()
logger = logging.getLogger("my_app")


auth_router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(id_usuario):
    token = f"GFJGN434N5JDNG{id_usuario}"
    return token

def autenticar_usuario(email: str, senha: str, session: Session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    
    
    return usuario


@auth_router.get(
    path="/",
    summary="Rota de autenticação",
    description="Rota inicial de autenticação",
    status_code=200,
    response_model=dict,
    responses={
        200: {
            "description": "Rota de autenticação acessada com sucesso",
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
    return {"message": "Rota de autenticação"}


@auth_router.post(
    path="/criar_conta", 
    summary="Criar uma nova conta de usuário",
    description="Rota para criação de uma nova conta de usuário",
    status_code=201,
    response_model=dict,
    responses={
        201: {
            "description": "Usuário criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Usuário criado com sucesso", 
                        "id": 1, 
                        "email": "user@example.com"
                    }
                }
            },
        },
        400: {
            "description": "Usuário já existe / dados inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Usuário já existe"
                    }
                }
            },
        },
        422: {
            "description": "Dados inválidos fornecidos (validação Pydantic)",
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
async def criar_conta(usuario_schema: UsuarioSchema, session: Session=Depends(pegar_sessao)):
    try:
        usuario = session.query(Usuario).filter_by(email=usuario_schema.email).first()

        if usuario:
            raise HTTPException(status_code=400, detail="Usuário já existe")
        else:
            senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
            
            novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
            ativo = usuario_schema.ativo if usuario_schema.ativo is not None else True
            admin = usuario_schema.admin if usuario_schema.admin is not None else False
            novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, ativo, admin)

            session.add(novo_usuario)
            session.commit()
            logger.info(f"POST criar_conta {usuario_schema.email} | 200 OK")
            return {"mensagem": f"usuario cadastrado com sucesso {usuario_schema.email}"}
    except Exception as e:
        logger.error(f"POST criar_conta {usuario_schema.email} | 500 ERRO | {traceback.format_exception(type(e), e, e.__traceback__)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor ao criar usuário")


@auth_router.post(
    path="/login",
    summary="Login de usuário",
    description="Rota para autenticação de usuário e geração de token",
    status_code=200,
    response_model=dict,
)
async def login(login_schema: LoginSchema, session: Session=Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token, "token_type": "bearer"}
