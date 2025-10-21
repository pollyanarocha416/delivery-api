from fastapi import APIRouter, Depends, HTTPException
from app.db.models import Usuario
from app.dependencies import pegar_sessao
import traceback
from app.main import bcrypt_context
from app.schemas.auth_schemas import UsuarioSchema
from sqlalchemy.orm import Session


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get(
    path="/"
)
async def home():
    """_summary_

    Returns:
        _type_: aaaaaaaaaaaa
    """
    return {"message": "Rota de autenticação"}


@auth_router.post(
    path="/criar_conta", 
    summary="Criar uma nova conta de usuário",
    status_code=201,
    response_model=dict,
    responses={
        201: {"description": "Usuário criado com sucesso"},
        500: {"description": "Erro interno do servidor"}
        }
)
async def criar_conta(usuario_schema: UsuarioSchema, session=Depends(pegar_sessao)):

    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()

    if usuario:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuario cadastrado com sucesso {usuario_schema.email}"}
