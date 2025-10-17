from fastapi import APIRouter, Depends
from app.db.models import Usuario
from app.dependencies import pegar_sessao

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get(
    path="/"
)
async def homr():
    """_summary_

    Returns:
        _type_: aaaaaaaaaaaa
    """
    return {"message": "Rota de autenticação"}


@auth_router.post(
    path="/criar_conta"
)
async def criar_conta(email: str, senha: str, nome: str, session=Depends(pegar_sessao)):
    
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        pass
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuario cadastrado com sucesso"}
    