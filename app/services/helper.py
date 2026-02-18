
from typing import cast
from app.db.models import Pedido, Usuario

class AuthorizationService:
    def can_modify_order(self, user: Usuario, order: Pedido) -> bool:
        is_owner: bool = cast(bool, user.id == order.id_usuario)
        is_admin: bool = cast(bool, user.admin == True)
        
        return is_admin or is_owner
