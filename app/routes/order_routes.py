import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Literal, Optional, cast
from sqlalchemy.orm import Session
from app.logging_config import setup_logging
from app.schemas.order_schemas import OrderResponse, OrderSchema
from app.db.models import Pedido, Usuario
from app.dependencies import pegar_sessao, verify_jwt_token
from jose import JWTError


setup_logging()
logger = logging.getLogger("my_app")

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_jwt_token)])


@order_router.get(
    path="/order",
    summary="Orders List",
    description="Returns all available orders (optional filter by status)",
    status_code=200,
    response_model=List[OrderResponse],
    responses= {
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "status": "CANCELADO",
                        "id_usuario": 1,
                        "preco": 25.5
                    }
                }
            }
        },
        "401": {
            "description": "Unauthorized Access",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authorized"
                    }
                }
            }
        },
        "404": {
            "description": "Additional Response",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No orders found"
                    }
                }
            }
        },
        "422": {
            "description": "Invalid data provided",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid status value"
                    }
                }
            }  
        }
    }
)
async def orders(status: Optional[Literal['PENDENTE', 'CANCELADO', 'FINALIZADO']] = None, session: Session = Depends(pegar_sessao)):
    try:
        if status:
            all_orders = session.query(Pedido).filter_by(status=status).all()
        else:
            all_orders = session.query(Pedido).all()
        return all_orders
    except Exception as e:
        logger.error(f"GET orders | 500 ERRO | {traceback.format_exception(type(e), e, e.__traceback__)}")
        raise HTTPException(status_code=500, detail="Internal server error.")


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
                        "detail": "Invalid input data"
                    }
                }
            }  
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Internal server error"
                    }
                }
            },
        }
    }
)
async def create_order(
    order_schema: OrderSchema, 
    session: Session=Depends(pegar_sessao),
    user: Usuario=Depends(verify_jwt_token)
    ):
    try:
        new_order = Pedido(usuario=order_schema.id_usuario)
        is_owner: bool = cast(bool, user.id == order_schema.id_usuario)
        
        is_admin: bool = cast(bool, user.admin == True)
        
        if not (is_admin or is_owner):
            logger.warning(f"POST create_order {order_schema.id_usuario} | 401 Not authorized")
            raise HTTPException(status_code=401, detail="Not authorized to create order for another user.")
        
        session.add(new_order)
        session.commit()
        
        logger.info(f"POST create_order {order_schema.id_usuario} | 201 Created")
        return {"message": f"Create order: {new_order.id}"}

    except JWTError as jwt_error:
        logger.error(f"POST criar_conta {order_schema.id_usuario} | 401 Unauthorized | {traceback.format_exception(type(jwt_error), jwt_error, jwt_error.__traceback__)}")
        raise HTTPException(status_code=401, detail="Token generation error.")
    except Exception as e:
        logger.error(f"POST criar_conta {order_schema.id_usuario} | 500 ERRO | {traceback.format_exception(type(e), e, e.__traceback__)}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error.")


@order_router.post(
    path="/order/cancel/{order_id}",
    description="Cancel an existing order",
    summary="Cancel order",
    status_code=200,
    response_model=dict,
    responses={
        200: {
            "description": "Order canceled successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Order 1 canceled successfully",
                        "order": {
                            "id": 1,
                            "status": "CANCELADO",
                            "price": 25.5
                        }
                    }
                }
            },
        },
        401: {
            "description": "Not authorized to cancel this order",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authorized to cancel this order | Admins only."
                    }
                }
            }
        },
        404: {
            "description": "Order not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Order not found"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Internal server error"
                    }
                }
            },
        }
    }
)
async def cancel_order(
    order_id: int, 
    session: Session=Depends(pegar_sessao),
    user: Usuario=Depends(verify_jwt_token)
):
    try:
        order = session.query(Pedido).filter(Pedido.id == order_id).first()
        if not order:
            logger.warning(f"POST cancel_order {order_id} | 404 Not Found")
            raise HTTPException(status_code=404, detail="Order not found")
        
        is_admin: bool = cast(bool, user.admin == True)
        is_owner: bool = cast(bool, user.id == order.id_usuario)
        
        if not (is_admin or is_owner):
            logger.warning(f"POST cancel_order {order_id} | 401 Not authorized")
            raise HTTPException(status_code=401, detail="Not authorized to cancel this order | Admins only.")
        
        
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
    except JWTError as jwt_error:
        logger.error(f"POST cancel_order {order_id} | 401 Unauthorized | {traceback.format_exception(type(jwt_error), jwt_error, jwt_error.__traceback__)}")
        raise HTTPException(status_code=401, detail="Token generation error.")
    except Exception as e:
        logger.error(f"POST cancel_order {order_id} | 500 ERRO | {traceback.format_exception(type(e), e, e.__traceback__)}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error.")
