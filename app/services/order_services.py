from fastapi import HTTPException
from app.db.models import Pedido
from app.services.helper import AuthorizationService


class OrderService:
        
    def get_order(self, status: str | None, session) -> list[Pedido]:
        if status:
            all_orders = session.query(Pedido).filter_by(status=status).all()
        else:
            all_orders = session.query(Pedido).all()
        if not all_orders:
            raise HTTPException(status_code=404, detail="No orders found")
        return all_orders
    
    def get_order_by_id(self, order_id: int, session) -> Pedido:
        order = session.query(Pedido).filter_by(id=order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    
    def create_order(self, order_schema, session, user):
        try:
            new_order = Pedido(usuario=order_schema.id_usuario)
        
            authorization_service = AuthorizationService()
            
            is_admin_or_owner: bool = authorization_service.can_access_order(user, new_order)
            
            if not is_admin_or_owner:
                raise HTTPException(status_code=401, detail="Not authorized to create order for another user.")
        
            session.add(new_order)
            session.commit()
        
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")