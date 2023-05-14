from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from .models import Base, CourierTypes

SQLALCHEMY_DATABASE_URL = 'postgresql://valeriaduborova@localhost:5432/lavka'
# SQLALCHEMY_DATABASE_URL = 'postgresql://root:root@localhost:5432/lavka'

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
