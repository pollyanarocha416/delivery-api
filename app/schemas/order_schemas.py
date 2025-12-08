from pydantic import BaseModel, Field
from typing import Literal, Optional


class OrderSchema(BaseModel):
    id_usuario: int = Field(..., description="ID do usuário que fez o pedido")

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    status: Literal['PENDENTE', 'CANCELADO', 'FINALIZADO']
    id_usuario: Optional[int] = None
    preco: Optional[float] = None

    class Config:
        from_attributes = True
        orm_mode = True
