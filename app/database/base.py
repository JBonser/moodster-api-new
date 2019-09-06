"""
This the core database initialisation file, it defines the declarative base
which is used by all the models to create the database schema. It also provides
the session object which is used by all the routes for database connection/querying.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app import config

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()


def init_database():
    Base.metadata.create_all(bind=engine)


def destroy_database():
    Base.metadata.drop_all(bind=engine)
