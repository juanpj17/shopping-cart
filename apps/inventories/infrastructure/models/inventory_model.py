from datetime import datetime
from sqlmodel import SQLModel, Field
from core.infrastructure.db_session.postgre_session import Session

session = Session()
target_metadata = SQLModel.metadata

class InventoryModel(SQLModel, table=True):  
    __tablename__: str = "inventory"  

    entity_id: str = Field(max_length=256, primary_key=True)  
    product_id: str = Field(index=True, max_length=256, nullable=False, unique=True)  
    quantity: int = Field(nullable=False, ge = 0)  
    created_at: datetime = Field(default_factory=datetime.now)  

    def __str__(self):
        return self.__tablename__