""" PostgreSQL database initializer """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model import Base

database_url = os.environ.get("DATABASE_URL")

engine = create_engine(database_url)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine, autoflush=False)
session = Session()
