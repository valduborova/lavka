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
    ordered_at: datetime
    delivery_price: int


class OrdersComplete(BaseModel):
    courier_id: int
    order_id: int
    delivered_at: str


class DateRange(BaseModel):
    start_date: str
    end_date: str


# todo: удалить этот эндпоинт
@router.get("/ping")
async def pong():
    return "pong"

@router.get("/clear_db")
async def clear_db():
    with SessionLocal() as db:
        db.query(models.Couriers).delete()
        db.query(models.Orders).delete()
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


@router.get(
    "/couriers/{courier_id}",
    status_code=status.HTTP_200_OK
)
async def get_courier_id(courier_id):
    entry = db.query(models.Couriers).get(courier_id)
    return entry


@router.get(
    "/couriers",
    status_code=status.HTTP_200_OK
)
async def get_couriers():
    entry = db.query(models.Couriers).all()

    return entry


@router.post(
    "/orders",
    status_code=status.HTTP_200_OK
)
async def post_orders(item: Orders):
    entry = models.Orders(order_id=item.order_id,
                          weight=item.weight,
                          region=item.region,
                          time_delievery=item.time_delievery,
                          price=item.price)
    db.add(entry)
    db.commit()
    db.close()


@router.get(
    "/orders/{order_id}",
    status_code=status.HTTP_200_OK
)
async def get_order_id(order_id):
    entry = db.query(models.Orders).get(order_id)

    return entry


@router.get(
    "/orders",
    status_code=status.HTTP_200_OK
)
async def get_orders(offset=0, limit=1):
    query = db.query(models.Orders)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    entry = query.all()

    return entry


@router.post(
    "/orders/complete"
)
async def post_complete(order: OrdersComplete):
    id = db.query(models.Couriers).get(order.courier_id)
    if id is None:
        return 'HTTP 400 Bad Request'
    else:
        db.query(Orders).\
            filter(Orders.order_id == order.order_id).\
            update(courier_id=order.courier_id,
                   order_time=order.order_time)
        db.commit()
        db.close()
        return 'HTTP 200 OK ' + str(order.order_id)


@router.get("/couriers/meta-info/{courier_id}")
async def get_meta(courier_id: int, daterange: DateRange):
    start_date = parser.parse(daterange.start_date)
    end_date = parser.parse(daterange.end_date)
    with SessionLocal() as session:
        courier = session.get(models.Couriers, courier_id)
        if courier is None:
            content = {"message": "Courier not found"}
            return Response(content, status_code=status.HTTP_404_NOT_FOUND)
        orders = session.query(models.Orders).\
            filter(models.Orders.courier_id == courier_id).\
            filter(models.Orders.ordered_at >= start_date).\
            filter(models.Orders.ordered_at < end_date).all()
    if not orders:
        content = {"message": f"Provided {courier_id=} does not have any orders in provided time period"}
        return Response(content, status_code=status.HTTP_200_OK)
    income = sum([order.delivery_price * courier.type.c_payment for order in orders])
    rating = len(orders) / (end_date - start_date).total_seconds() / 3600 * courier.type.c_rating
    content = {"income": income, "rating": rating}
    return Response(content, status_code=status.HTTP_200_OK)
