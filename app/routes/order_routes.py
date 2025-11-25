import logging
import pdb
import traceback
from typing import List, Literal, Optional
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.order_schemas import OrderResponse, OrderSchema
from app.dependencies import pegar_sessao, verify_jwt_token
from sqlalchemy.orm import Session
from app.db.models import Pedido
from app.logging_config import setup_logging


setup_logging()
logger = logging.getLogger("my_app")

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_jwt_token)])

@order_router.get(
    path="/order",
    summary="Rota order",
    description="Retorna todas as ordens disponíveis (opcional filtro por status)",
    status_code=200,
    response_model=List[OrderResponse],
)
async def orders(status: Optional[Literal['PENDENTE', 'CANCELADO', 'FINALIZADO']] = None, session: Session = Depends(pegar_sessao)):
    if status:
        all_orders = session.query(Pedido).filter_by(status=status).all()
    else:
        all_orders = session.query(Pedido).all()
    return all_orders



@order_router.post(
    path="/order",
    description="Create a new order",
    summary="Create order",
    status_code=201,
    response_model=dict,
    responses={
        201: {
            "description": "Order created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Create order: 1"
                    }
                }
            },
        },
        422: {
            "description": "Invalid data provided",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Dados invalidos"
                    }
                }
            }  
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Erro interno da API"
                    }
                }
            },
        }
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



@order_router.post("/order/cancel/{order_id}")
async def cancel_order(
    order_id: int, 
    session: Session=Depends(pegar_sessao)
):
    order = session.query(Pedido).filter(Pedido.id == order_id).first()
    if not order:
        logger.warning(f"POST cancel_order {order_id} | 404 Not Found")
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = "CANCELADO"
    session.commit()
    logger.info(f"POST cancel_order {order_id} | 200 OK")
    return {
        "message": f"Order {order_id} canceled successfully",
        "order": {
            "id": order.id,
            "status": order.status,
            "price": order.preco
        }
    }
