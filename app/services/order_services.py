from fastapi import HTTPException
from app.db.models import Pedido

class OrderService:
        
    def get_order(self, status, session):
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
