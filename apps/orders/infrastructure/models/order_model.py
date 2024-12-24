from datetime import datetime
from sqlmodel import SQLModel, Field
from core.infrastructure.db_session.postgre_session import Session

session = Session()
target_metadata = SQLModel.metadata

class OrderModel(SQLModel, table=True):  
    __tablename__: str = "order"  

    entity_id: str = Field(max_length=256, primary_key=True)  
    user_id: str = Field(max_length=256, nullable=False)  
    cart_id: str = Field(max_length=256, nullable=False)  
    status: str = Field(max_length=32, nullable=False)  
    total: str = Field(max_length=128, nullable=False)  
    created_at: datetime = Field(default_factory=datetime.now)  

    def __str__(self):
        return self.__tablename__