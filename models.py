from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List

DATABASE_URL = "sqlite:///./test.db"
Base = declarative_base()

class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True

class Database:
    def __init__(self, url: str = DATABASE_URL):
        self.engine = create_engine(url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Create the database tables
        Base.metadata.create_all(bind=self.engine)

    def initialize(self):
        # This method is not used in this example, but you can use it if needed
        pass

# Create an instance of the Database class
db = Database()

# Create a Session class for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db.engine)
