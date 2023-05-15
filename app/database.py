from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.exc import ProgrammingError

from .models import Base, CourierTypes

# SQLALCHEMY_DATABASE_URL = 'postgresql://valeriaduborova@localhost:5432/lavka'
# SQLALCHEMY_DATABASE_URL = 'postgresql://root:root@localhost:5432/lavka'


PG_USER = 'postgres'
PG_PASSWORD = 'password'
PG_HOST = 'db'
PG_PORT = '5432'
PG_DATABASE = 'PostgreSQL 15.2'

SQLALCHEMY_URL = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}'
SQLALCHEMY_DATABASE_URL = f'{SQLALCHEMY_URL}/{PG_DATABASE}'


with create_engine(f"{SQLALCHEMY_URL}/postgres").connect() as conn:
    conn.execute(text('COMMIT'))
    try:
        conn.execute(text(f'CREATE DATABASE "{PG_DATABASE}"'))
        conn.execute(text('COMMIT'))
    except ProgrammingError:
        pass


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


with SessionLocal() as session:
    if not session.query(CourierTypes).first():
        session.add_all([
            CourierTypes(type_id='foot', c_payment=2, c_rating=3),
            CourierTypes(type_id='bike', c_payment=3, c_rating=2),
            CourierTypes(type_id='car', c_payment=4, c_rating=1)
        ])
        session.commit()
