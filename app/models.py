from sqlalchemy import (ARRAY, CheckConstraint, Column, DateTime, Float,
                        ForeignKey, Integer, String)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class CourierTypes(Base):
    __tablename__ = 'couriertypes'

    type_id = Column(String, primary_key=True)
    c_payment = Column(Float)
    c_rating = Column(Float)
    CheckConstraint('type_id IN ("foot", "bike", "car")',
                    name='type_check')
    CheckConstraint('c_payment >= 0', name='payment_check')
    CheckConstraint('c_rating >= 0', name='rating_check')

    def __repr__(self):
        return f'<CourierTypes(type_id={self.type_id}, c_payment={self.c_payment}, " \
            "c_rating={self.c_rating})>'


class Couriers(Base):
    __tablename__ = 'couriers'

    courier_id = Column(Integer, primary_key=True)
    region = Column(Integer)
    type_id = Column(String, ForeignKey('couriertypes.type_id'))
    type = relationship('CourierTypes', backref='couriers')
    working_graphics = Column(ARRAY(String))

    def __repr__(self):
        return f'<Couriers(courier_id={self.courier_id}, region={self.region}, " \
            "type_id={self.type_id}, working_graphics={self.working_graphics})>'



class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    weight = Column(Integer)
    region = Column(Integer)
    ordered_at = Column(DateTime)
    delivery_price = Column(Integer)
    # Extra fields
    courier_id = Column(Integer, ForeignKey('couriers.courier_id'), nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    CheckConstraint('weight >= 0', name='weight_check')
    CheckConstraint('price >= 0', name='price_check')

    def __repr__(self):
        return f'<Orders(order_id={self.order_id}, weight={self.weight}, region={self.region}, " \
            "ordered_at={self.ordered_at}, price={self.delivery_price}, courier_id={self.courier_id}, " \
            "delivered_at={self.delivered_at})>'

