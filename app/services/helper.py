from typing import cast
from app.db.models import Pedido, Usuario

class AuthorizationService:

    def is_owner(self, user: Usuario, order: Pedido) -> bool:
        return cast(bool, user.id == order.id_usuario)
    
    def is_admin(self, user: Usuario) -> bool:
        return cast(bool, user.admin == True)
    
    def can_access_order(self, user: Usuario, order: Pedido) -> bool:
        return self.is_owner(user, order) or self.is_admin(user)
