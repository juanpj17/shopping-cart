from datetime import datetime
from sqlmodel import Session, select, delete, SQLModel
from sqlalchemy.exc import SQLAlchemyError
from ...domain.product import Product
from ...domain.repositories.product_repository import ProductRepository
from ..models.product_model import ProductModel
from core.infrastructure.db_session.postgre_session import DBSession

class PostgreProductRepository(ProductRepository):
    def __init__(self, product_model: SQLModel):
        self.product_model = product_model
        self.session = DBSession.get_session()

    def save_product(self, product: Product):
        try:
            existing_product = self.get_product_by_id(product._id)

            if existing_product:
                if existing_product.name != product.name:
                    existing_product.name = product.name 
                if existing_product.price != product.price:
                    existing_product.price = product.price
                if existing_product.cost != product.cost:
                    existing_product.cost = product.cost
                if existing_product.margin != product.margin:
                    existing_product.margin = product.margin
                existing_product.updated_at=datetime.now()
            else:
                existing_product = ProductModel(
                    entity_id=product._id,
                    code = product.code,
                    name = product.name,
                    description = product.description,
                    price = product.price,
                    cost = product.cost,
                    margin = product.margin,
                    status = product.status,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                self.session.add(existing_product)
            self.session.commit()
            self.session.refresh(existing_product)  
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Error saving the product: {e}")
        

    def remove_product(self, id):
        statement = delete(ProductModel).where(ProductModel.entity_id == id)
        self.session.exec(statement)
        self.session.commit()

    def get_product_by_id(self, id):
        statement = select(ProductModel).where(ProductModel.entity_id == id)
        product = self.session.exec(statement).first()
        return product
    
    def get_all_products(self):
        statement = select(ProductModel)
        product = self.session.exec(statement).all()
        return product
        
        