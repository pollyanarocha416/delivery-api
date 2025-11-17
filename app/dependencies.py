from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from app.db.models import db
from app.db.models import Usuario


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verify_jwt_token(token: str, session: Session=Depends(pegar_sessao)):
    user = session.query(Usuario).filter(Usuario.id==1).first()
    
    return user
