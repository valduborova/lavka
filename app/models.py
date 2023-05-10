from sqlalchemy import ARRAY, CheckConstraint, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Couriers(Base):
    __tablename__ = 'Couriers'

    courier_id = Column(Integer, primary_key=True)
    region = Column(Integer)
    type = Column(String)
    working_graphics = Column(ARRAY(String))
    CheckConstraint('type="foot" OR type="bike" OR type="car"',
                    name='type_check')


class Orders(Base):
    __tablename__ = 'Orders'

    order_id = Column(Integer, primary_key=True)
    weight = Column(Integer)
    region = Column(Integer)
    time_delievery = Column(String)
    price = Column(Integer)
