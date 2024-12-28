from datetime import datetime
from sqlmodel import SQLModel, Field
from core.infrastructure.db_session.postgre_session import Session

session = Session()
target_metadata = SQLModel.metadata

class UserModel(SQLModel, table=True):  
    __tablename__: str = "user"  

    entity_id: str = Field(max_length=256, primary_key=True)  
    username: str = Field(index=True, max_length=32, nullable=False, unique=True)  
    email: str = Field(max_length=32, nullable=False)  
    password: str = Field(max_length=128, nullable=False)  
    role: str = Field(max_length=32, nullable=False)  
    created_at: datetime = Field(default_factory=datetime.now)  
    updated_at: datetime = Field(default_factory=datetime.now)  

    def __str__(self):
        return self.__tablename__
