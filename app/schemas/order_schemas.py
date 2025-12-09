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


class ItemOrderSchema(BaseModel):
    quantidade: int = Field(..., description="Quantidade do item no pedido")
    sabor: str = Field(..., description="Sabor do item no pedido")
    tamanho: str = Field(..., description="Tamanho do item no pedido")
    preco_unitario: float = Field(..., description="Preço unitário do item no pedido")

class Config:
        from_attributes = True
        orm_mode = True
