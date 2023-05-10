from fastapi import APIRouter, Request
from starlette import status
from pydantic import BaseModel

from .database import SessionLocal
from app import models


router = APIRouter()
db = SessionLocal()


class Couriers(BaseModel):
    courier_id: int
    region: int
    type: str
    working_graphics: str

class Orders(BaseModel):
    order_id: int
    weight: int
    region: int
    time_delievery: str
    price: int

@router.post(
    "/couriers",
    status_code=status.HTTP_200_OK
)
async def post_couriers(item: Couriers):
    entry = models.Couriers(courier_id=item.courier_id,
                            region=item.region,
                            type=item.type,
                            working_graphics=item.working_graphics)
    # try:
    db.add(entry)
    db.commit()
    db.close()
        # return redirect('/posts')
    # except:
    #     return 'При добавлении записи произошла ошибка'
    # return item.name


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
    # try:
    db.add(entry)
    db.commit()
    db.close()
        # return redirect('/posts')
    # except:
    #     return 'При добавлении записи произошла ошибка'
    # return item.name


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
async def get_orders():
    entry = db.query(models.Orders).all()

    return entry


@router.post(
    "/orders/complete"
)
async def post_complete():
    return 'pong'

