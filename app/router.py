from datetime import datetime
from enum import Enum
from typing import List

from dateutil import parser
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, constr

from app import models
from app.database import SessionLocal

router = APIRouter()


class CourierTypes(str, Enum):
    foot = "foot"
    bike = "bike"
    car = "car"

    def __str__(self):
        return self.name


class Couriers(BaseModel):
    courier_id: int
    region: int
    type_id: CourierTypes
    working_graphics: List[constr(regex=r'^([01][0-9]|2[0-3]):[0-5][0-9]-([01][0-9]|2[0-3]):[0-5][0-9]$')]


class Orders(BaseModel):
    order_id: int
    weight: int
    region: int
    ordered_at: str
    delivery_price: int


class OrdersComplete(BaseModel):
    order_id: int
    courier_id: int
    delivered_at: str


class DateRange(BaseModel):
    start_date: str
    end_date: str


@router.get("/clear_db")
async def clear_db():
    with SessionLocal() as db:
        db.query(models.Orders).delete()
        db.query(models.Couriers).delete()
        db.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.post("/couriers")
async def post_couriers(items: List[Couriers]):
    ids = set()
    with SessionLocal() as session:
        for item in items:
            if item.courier_id in ids:
                content = {"message": "courier_id already exists", "courier_id": item.courier_id}
                return JSONResponse(content, status_code=status.HTTP_400_BAD_REQUEST)
            ids.add(item.courier_id)
        for item in ids:
            if session.get(models.Couriers, item):
                content = {"message": "courier_id already exists", "courier_id": item}
                return JSONResponse(content, status_code=status.HTTP_400_BAD_REQUEST)
        for item in items:
            entry = models.Couriers(courier_id=item.courier_id,
                                    region=item.region,
                                    type_id=item.type_id.__str__(),
                                    working_graphics=item.working_graphics)
            session.add(entry)
        session.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.get("/couriers/{courier_id}")
async def get_courier_id(courier_id):
    with SessionLocal() as db:
        if not db.get(models.Couriers, courier_id):
            content = {"message": "no such courier_id", "courier_id": courier_id}
            return JSONResponse(content, status_code=status.HTTP_400_BAD_REQUEST)
    return db.query(models.Couriers).get(courier_id) 


@router.get("/couriers")
async def get_couriers(offset=0, limit=1):
    with SessionLocal() as db:
        query = db.query(models.Orders)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        entry = query.all()
    return entry


@router.post("/orders")
async def post_orders(items: List[Orders]):
    ids = set()
    with SessionLocal() as session:
        for item in items:
            if item.order_id in ids:
                content = {"message": "order_id already exists", "order_id": item.order_id}
                return JSONResponse(content, status_code=status.HTTP_400_BAD_REQUEST)
            ids.add(item.order_id)
        for item in ids:
            if session.get(models.Orders, item):
                content = {"message": "order_id already exists", "order_id": item}
                return JSONResponse(content, status_code=status.HTTP_400_BAD_REQUEST)
        for item in items:
            date = parser.parse(item.ordered_at)
            entry = models.Orders(order_id=item.order_id,
                          weight=item.weight,
                          region=item.region,
                          ordered_at=date,
                          delivery_price=item.delivery_price)
            session.add(entry)
        session.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.get("/orders/{order_id}")
async def get_order_id(order_id):
    with SessionLocal() as db:
        if not db.get(models.Orders, order_id):
            content = {"message": "no such courier_id", "courier_id": order_id}
            return JSONResponse(content, status_code=status.HTTP_400_BAD_REQUEST)
    return db.query(models.Orders).get(order_id) 


@router.get("/orders")
async def get_orders(offset: int = 0, limit: int = 1):
    with SessionLocal() as db:
        query = db.query(models.Orders)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        entry = query.all()
    content = [item.__dict__ for item in entry]
    for item in content:
        item.pop('_sa_instance_state')
        item.pop('courier_id')
        item.pop('delivered_at')
    return content


@router.post("/orders/complete")
async def post_complete(item: OrdersComplete):
    with SessionLocal() as session:
        if not session.query(models.Orders).get(item.order_id):
            content = {"message": "no such order_id", "order_id": item}
            return JSONResponse(content, status_code=status.HTTP_400_BAD_REQUEST)
        date = parser.parse(item.delivered_at)
        session.query(models.Orders).\
        filter(models.Orders.order_id == item.order_id).\
        update({models.Orders.courier_id: item.courier_id,
            models.Orders.delivered_at: date})
        session.commit()
        content = {"order_id": item.order_id}
        return JSONResponse(content, status_code=status.HTTP_200_OK)


@router.get("/couriers/meta-info/{courier_id}")
async def get_meta(courier_id: int, start_date: str, end_date: str):
    start = parser.parse(start_date)
    end = parser.parse(end_date)
    if start > end:
        content = {"message": "start_date must be earlier than end_date"}
        return JSONResponse(content, status_code=status.HTTP_400_BAD_REQUEST)
    with SessionLocal() as session:
        courier = session.get(models.Couriers, courier_id)
        if courier is None:
            content = {"message": f"Provided {courier_id=} not found"}
            return JSONResponse(content, status_code=status.HTTP_404_NOT_FOUND)
        orders = session.query(models.Orders).\
            filter(models.Orders.courier_id == courier_id).\
            filter(models.Orders.delivered_at >= start).\
            filter(models.Orders.delivered_at < end).all()
        if not orders:
            content = {"message": f"Provided {courier_id=} does not have any orders in provided time period"}
            return JSONResponse(content, status_code=status.HTTP_200_OK)
        income = sum(order.delivery_price * courier.type.c_payment for order in orders)
        rating = len(orders) / ((end - start).total_seconds() // 3600) * courier.type.c_rating
    content = {"income": income, "rating": rating}
    return JSONResponse(content, status_code=status.HTTP_200_OK)
