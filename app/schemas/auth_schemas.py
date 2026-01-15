from pydantic import BaseModel, Field
from typing import Optional


class UserSchema(BaseModel):
    nome: str = Field(..., min_length=1, max_length=45, description="Nome do usuário")
    email: str = Field(..., min_length=5, max_length=100, description="Email do usuário")
    senha: str = Field(..., min_length=3, max_length=45, description="Senha do usuário")
    ativo: Optional[bool] = Field(None, description="Indica se o usuário está ativo")
    admin: Optional[bool] = Field(None, description="Indica se o usuário tem privilégios de administrador")
    
    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str = Field(..., min_length=5, max_length=100, description="Email do usuário")
    senha: str = Field(..., min_length=3, max_length=45, description="Senha do usuário")
    
    class Config:
        from_attributes = True
