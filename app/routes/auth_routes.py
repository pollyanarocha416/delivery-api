from fastapi import APIRouter, Depends
from app.db.models import Usuario
from app.dependencies import pegar_sessao
import traceback


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
async def criar_conta(email: str, senha: str, nome: str, session=Depends(pegar_sessao)):
    try:
        usuario = session.query(Usuario).filter(Usuario.email==email).first()
        if usuario:
            pass
        else:
            novo_usuario = Usuario(nome, email, senha)
            session.add(novo_usuario)
            session.commit()
            return {"mensagem": "usuario cadastrado com sucesso"}
    except Exception as e:
        return {"erro": f"Erro ao criar usuário | {e}", "detalhes": traceback.format_exc()}
