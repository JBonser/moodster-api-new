"""
This the core database initialisation file, it defines the declarative base
which is used by all the models to create the database schema. It also provides
the session object which is used by all the routes for database connection/querying.
"""
from datetime import datetime
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import DateTime

from app import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseClass(object):
    """
    Generic Base Class for adding fields that should be available
    on every table in the database
    """

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


Base = declarative_base(cls=BaseClass)
