import traceback
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.main import SECRET_KEY, ALGORITHM, oath2_scheme
from app.db.models import db
from app.db.models import Usuario


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verify_jwt_token(token: str = Depends(oath2_scheme), session: Session=Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dic_info.get("sub"))
        
        user = session.query(Usuario).filter(Usuario.id==user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")   
