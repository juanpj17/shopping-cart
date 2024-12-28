from datetime import datetime
from sqlmodel import select, SQLModel
from sqlalchemy.exc import SQLAlchemyError
from ...domain import User, UserRepository
from ..models.user_model import UserModel
from core.infrastructure.db_session.postgre_session import DBSession

class PostgreUserRepository(UserRepository):
    def __init__(self, user_model: SQLModel):
        self.user_model = user_model
        self.session = DBSession.get_session()

    def save_user(self, user: User):
        try:
            existing_user = self.get_user_by_id(user._id)

            if existing_user:
                if existing_user.username != user.username:
                    existing_user.username = user.username 
                if existing_user.email != user.email:
                    existing_user.email = user.email
                if existing_user.password != user.password:
                    existing_user.password = user.password
                existing_user.updated_at=datetime.now()
                
            else:
                existing_user = UserModel(
                    entity_id=user._id,
                    username=user.username,
                    email=user.email,
                    password=user.password,
                    role=user.role,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                self.session.add(existing_user)
            self.session.commit()
            self.session.refresh(existing_user)  
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Error saving the user: {e}")

    def get_all_users(self):
        statement = select(UserModel).where(UserModel.role == "Manager")
        results = self.session.exec(statement)
        return results.all()
    
    def get_user_by_username(self, username):
        statement = select(UserModel).where(UserModel.username == username)
        result = self.session.exec(statement).first()  
        return result
    
    def get_user_by_id(self, id):
        statement = select(UserModel).where(UserModel.entity_id == id)
        result = self.session.exec(statement).first()
        return result 
    
    def find_admin_user(self):
        statement = select(UserModel)
        results = self.session.exec(statement)
        return results.all()
            
