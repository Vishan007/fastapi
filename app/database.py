from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings 

"""
SQLAlchemy is a popular SQL toolkit and Object Relational Mapper. 
It is written in Python and gives full power and flexibility of SQL to an application developer. 
"""

#CONNECTION_STRING_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base() 

def get_db(): ##responsible for connection
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


