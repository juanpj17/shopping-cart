from ...domain.repositories.inventory_repository import InventoryRepository
from ..models.inventory_model import InventoryModel
from datetime import datetime
from core.infrastructure.db_session.postgre_session import DBSession
from sqlmodel import select, SQLModel
from ..models.inventory_model import InventoryModel
from sqlalchemy.exc import SQLAlchemyError
from ...domain.inventory import Inventory

class PostgreInventoryRepository(InventoryRepository):

    def __init__(self, inventory_model: SQLModel):
        self.inventory_model = inventory_model
        self.session = DBSession.get_session()

    def save_inventory(self, inventory: Inventory):
        try:
            existing_inventory = self.get_inventory_by_product(inventory.product_id)
            if existing_inventory:
                if existing_inventory.quantity != inventory.quantity:
                    existing_inventory.quantity = inventory.quantity
                existing_inventory.updated_at = datetime.now()
            else:
                new_inventory = InventoryModel(
                    entity_id=inventory._id,
                    product_id=inventory.product_id,
                    quantity=inventory.quantity,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                self.session.add(new_inventory)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Error saving the inventory: {e}")
        
    def get_inventory_by_product(self, id):
        statement = select(InventoryModel).where(InventoryModel.product_id == id)
        response = self.session.exec(statement).first()
        return response
        
    
    def get_all(self):
        statement = select(InventoryModel)
        response = self.session.exec(statement).all()
        return response