from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

SQLALCHEMY_DATABASE_URL = 'postgresql://valeriaduborova@localhost:5432/lavka'
# SQLALCHEMY_DATABASE_URL = 'postgresql://root:root@localhost:5432/lavka'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
