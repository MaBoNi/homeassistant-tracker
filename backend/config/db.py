# backend/config/db.py

"""
Database configuration and initialization using SQLAlchemy.
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
)
Session = sessionmaker(bind=engine)


def init_db(drop_and_recreate=False):
    """
    Initialize the database schema. Optionally drops all tables before recreating.

    Args:
        drop_and_recreate (bool): If True, drops all tables before creating them.
    """
    if drop_and_recreate:
        Base.metadata.drop_all(engine)
        logger.info("Dropped all tables in the database.")

    Base.metadata.create_all(engine)
    logger.info("Initialized database with the current schema.")
