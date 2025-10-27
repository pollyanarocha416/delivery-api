from pydantic import BaseModel, Field
from typing import Optional


class OrderSchema(BaseModel):
    id_usuario: int = Field(..., description="ID do usuário que fez o pedido")

    class Config:
        from_attributes = True
