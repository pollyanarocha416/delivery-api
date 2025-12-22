from pydantic import BaseModel, Field
from typing import Literal, Optional


class OrderSchema(BaseModel):
    id_usuario: int = Field(..., description="ID do usuário que fez o pedido")

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int = Field(..., description="ID do pedido")
    status: Literal['PENDENTE', 'CANCELADO', 'FINALIZADO'] = Field(..., description="Status do pedido")
    id_usuario: Optional[int] = Field(None, description="ID do usuário que fez o pedido")
    preco: Optional[float] = Field(None, description="Preço total do pedido")

    class Config:
        from_attributes = True
        orm_mode = True


class ItemOrderSchema(BaseModel):
    quantidade: int = Field(..., ge=1, le=100, description="Quantidade do item no pedido")
    sabor: str = Field(..., min_length=1, max_length=45, description="Sabor do item no pedido")
    tamanho: str = Field(..., min_length=1, max_length=45, description="Tamanho do item no pedido")
    preco_unitario: float = Field(..., gt=0, description="Preço unitário do item no pedido")

    class Config:
        from_attributes = True
        orm_mode = True
