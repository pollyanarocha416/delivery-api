from typing import cast
from fastapi import HTTPException
from app.db.models import Pedido

class OrderService:

    def validations(self, user):
        
        is_admin: bool = cast(bool, user.admin == True)
        
        if not is_admin:
            raise HTTPException(status_code=401, detail="Not authorized")
        
    def get_order(self, status, user, session):
        self.validations(user)
        
        if status:
            all_orders = session.query(Pedido).filter_by(status=status).all()
        else:
            all_orders = session.query(Pedido).all()
        return all_orders
    
    def get_order_by_id(self, order_id, session):
        
        order = session.query(Pedido).filter_by(id=order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
