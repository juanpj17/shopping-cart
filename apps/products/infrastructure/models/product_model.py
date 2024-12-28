from datetime import datetime
from sqlmodel import SQLModel, Field
from core.infrastructure.db_session.postgre_session import Session

session = Session()
target_metadata = SQLModel.metadata

class ProductModel(SQLModel, table=True):  
    __tablename__: str = "product"  

    entity_id: str = Field(max_length=256, primary_key=True)  
    code: str = Field(index=True, max_length=256, nullable=False, unique=True)  
    name: str = Field(max_length=64, nullable=False)  
    description: str = Field(max_length=256, nullable=True)
    price: float = Field(nullable=False, gt = 0)  
    cost: float = Field(nullable=False, gt = 0)
    margin: float = Field(nullable=False, ge = 0)  
    status: str = Field(max_length=32, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)  
    updated_at: datetime = Field(default_factory=datetime.now)

    def __str__(self):
        return self.__tablename__