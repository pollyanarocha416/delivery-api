from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get(
    path="/"
)
async def auth():
    """_summary_

    Returns:
        _type_: aaaaaaaaaaaa
    """
    return {"message": "Rota de autenticação"}
