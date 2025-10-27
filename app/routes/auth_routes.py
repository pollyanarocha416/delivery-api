import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import pegar_sessao
from app.main import bcrypt_context
from app.schemas.auth_schemas import UsuarioSchema
from app.schemas.auth_schemas import LoginSchema
from app.db.models import Usuario


auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario):
    token = f"GFJGN434N5JDNG{id_usuario}"
    return token


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
async def criar_conta(usuario_schema: UsuarioSchema, session: Session=Depends(pegar_sessao)):

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
        return {"mensagem": f"usuario cadastrado com sucesso {usuario_schema.email}"}



@auth_router.post(
    path="/login",
    summary="Login de usuário",
    status_code=200,
)
async def login(login_schema: LoginSchema, session: Session=Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter_by(email=login_schema.email).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token, "token_type": "bearer"}
