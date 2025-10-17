from sqlalchemy.orm import sessionmaker
from app.db.models import db

def pegar_sessao():
    Session = sessionmaker(bind=db)
    session = Session()
    return session
