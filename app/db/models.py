from typing import Optional
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
# from sqlalchemy_utils.types import ChoiceType


db = create_engine(url="sqlite:///banco.db")

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id    = Column("id", Integer, primary_key=True, autoincrement=True)
    nome  = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome: str, email: str, senha: str, ativo: Optional[bool] = True, admin: Optional[bool] = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__ = "pedidos"
    
    # STATUS_PEDIDOS = (
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # )
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    id_usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    # itens = 
    
    def __init__(self, usuario: int, status: str = "PENDENTE", preco: float = 0):
        self.id_usuario = usuario
        self.preco = preco
        self.status = status


class ItensPedido(Base):
    __tablename__ = "itens_pedido"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))
    
    
    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
