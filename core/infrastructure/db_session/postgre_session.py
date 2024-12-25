from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
from pathlib import Path
from os import getenv

env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

engine = create_engine(getenv("DATABASE_URL"))
class DBSession:

    @staticmethod
    def get_session():
        return Session(engine)
    