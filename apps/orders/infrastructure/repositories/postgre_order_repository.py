from datetime import datetime
from sqlmodel import select, SQLModel
from sqlalchemy.exc import SQLAlchemyError
from core.infrastructure.db_session.postgre_session import DBSession
from ..models.order_model import OrderModel
from ...domain.repositories.order_repository import OrderRepository
from ...domain.order import Order

class PostgreOrderRepository(OrderRepository):
    def __init__(self, order_model: SQLModel):
        self.session = DBSession.get_session()
        self.order_model = order_model
    
    def save_order(self, order: Order):
        order_exist = self.get_order_by_id(order._id)
        try:
            if not order_exist:
                new_order = OrderModel(
                    entity_id = order._id,
                    user_id = order.user_id,
                    cart_id = order.cart_id,
                    status = order.status,
                    total = order.total,
                    created_at = datetime.now()            
                ) 
                self.session.add(new_order)
            else:
                if order.status: order_exist.status = order.status
                if order.total: order_exist.total = order.total
            
            self.session.commit()
        except SQLAlchemyError as error:
            self.session.rollback()
            raise RuntimeError(f"Error saving the order: {error}")
    
    def get_order_by_id(self, order_id: str):
        statement = select(self.order_model).where(self.order_model.entity_id == order_id)
        try:
            res = self.session.exec(statement).first()
            return res
        except SQLAlchemyError as error:
            self.session.rollback()
            raise RuntimeError(f"Error searching the order: {error}")
        
    def get_all_orders(self):
        statement = select(self.order_model)
        try:
            res = self.session.exec(statement).all()
            return res
        except SQLAlchemyError as error:
            self.session.rollback()
            raise RuntimeError(f"Error searching all orders: {error}")