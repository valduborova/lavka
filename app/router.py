from fastapi import APIRouter, Request
from starlette import status
from pydantic import BaseModel, constr

from .database import SessionLocal
from app import models


router = APIRouter()
db = SessionLocal()


class Couriers(BaseModel):
    courier_id: int
    region: int
    type: str
    working_graphics: constr(regex=r'^([01][0-9]|2[0-3]):[0-5][0-9]-([01][0-9]|2[0-3]):[0-5][0-9]$')


class Orders(BaseModel):
    order_id: int
    weight: int
    region: int
    time_delievery: str
    price: int


class OrdersComplete(BaseModel):
    courier_id: int
    order_id: int
    order_time: str


class Date(BaseModel):
    date: constr(regex=r'^\d{4}-\d{2}-\d{2}$')



@router.post(
    "/couriers",
    status_code=status.HTTP_200_OK
)
async def post_couriers(item: Couriers):
    entry = models.Couriers(courier_id=item.courier_id,
                            region=item.region,
                            type=item.type,
                            working_graphics=item.working_graphics)
    db.add(entry)
    db.commit()
    db.close()


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
                            price = item.price)
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
async def get_orders(offset = 0, limit = 1):
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
        return 'HTTP 200 OK ' + str(order.order_id)


@router.get(
    "/couriers/meta-info/{courier_id}"
)
async def f(start_date, end_date):
    pass
async def income():
    pass
async def rating():
    pass
