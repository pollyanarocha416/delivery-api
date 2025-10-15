from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])


@order_router.get(
    path="/",
    summary="Rota order",
    description="endpoint de rotas order",
    status_code=200,
    response_model=dict,
    responses={}
)
async def orders():
    return {"message": "Router order"}
