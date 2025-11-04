import logging
import traceback
from fastapi import APIRouter, Depends
from app.schemas.order_schemas import OrderSchema
from app.dependencies import pegar_sessao
from sqlalchemy.orm import Session
from app.db.models import Pedido
from app.logging_config import setup_logging


setup_logging()
logger = logging.getLogger("my_app")

order_router = APIRouter(prefix="/orders", tags=["orders"])


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




@order_router.post(
    path="/order",
    description="Create a new order",
    summary="Create order",
    status_code=201,
    response_model=dict,
    responses={
        201: {"description": "Order created successfully"},
        500: {"description": "Internal server error"},
        422: {"description": "Invalid data provided"}
    }
    )
async def create_order(order_schema: OrderSchema, session: Session=Depends(pegar_sessao)):
    try:
        new_order = Pedido(usuario=order_schema.id_usuario)
        session.add(new_order)
        session.commit()
        
        logger.info(f"POST create_order {order_schema.id_usuario} | 201 Created")
        return {"message": f"Create order: {new_order.id}"}
    except Exception as e:
        logger.error(f"POST criar_conta {order_schema.id_usuario} | 500 ERRO | {traceback.format_exception(type(e), e, e.__traceback__)}")
        session.rollback()
        raise e
