from datetime import datetime
from sqlmodel import SQLModel, Field
from core.infrastructure.db_session.postgre_session import Session

session = Session()
target_metadata = SQLModel.metadata


class CartModel(SQLModel, table=True):
    __tablename__: str = "cart"

    entity_id: str = Field(max_length=256, primary_key=True)  
    user_id: str = Field(max_length=256, nullable=False)  
    order_id: str = Field(max_length=256, nullable=True, unique=True)   
    is_archived: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)  

    def __str__(self):
        return self.__tablename__

class ProductCartModel(SQLModel, table=True):
    __tablename__: str = "product_cart"
  
    id: str = Field(max_length=256, primary_key=True)  
    cart_id: str = Field(max_length=256, nullable=False)  
    product_id: str = Field(max_length=256, nullable=True) 
    quantity: int = Field(nullable=False, ge = 0)  
    unit_price: float = Field(nullable=False, ge = 0) 
    created_at: datetime = Field(default_factory=datetime.now)  

    def __str__(self):
        return self.__tablename__