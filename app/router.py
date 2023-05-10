from fastapi import APIRouter, Request
from starlette import status
from pydantic import BaseModel

from .database import SessionLocal
from app import models


router = APIRouter()
db = SessionLocal()


class Courier(BaseModel):
    courier_id: int
    region: int
    type: str
    working_graphics: str

class Order(BaseModel):
    order_id: int
    weight: int
    region: int
    time_delievery: str
    price: int

# @router.get(
#     "/ping",
#     name='dev:ping',
#     status_code=status.HTTP_200_OK
# )
# async def ping():
#     return 'pong'


# @router.post(
#     "/hello",
#     name='dev:hello-username',
#     status_code=status.HTTP_200_OK
# )
# async def ping(request: Request):
#     request = await request.json()
#     username = request['username']
#     return f'Hello, {username}!'


@router.post(
    "/couriers",
    status_code=status.HTTP_200_OK
)
async def post_couriers(item: Courier):
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
    return courier_id


# @router.get(
#     "/couriers",
#     status_code=status.HTTP_200_OK
# )
# async def get_couriers():
#     return 'pong'


@router.post(
    "/orders",
    status_code=status.HTTP_200_OK
)
async def post_orders():
    return 'pong'


@router.get(
    "/orders/{order_id}",
    status_code=status.HTTP_200_OK
)
async def get_order_id():
    return 'pong'


@router.get(
    "/orders",
    status_code=status.HTTP_200_OK
)
async def get_orders():
    return 'pong'


@router.post(
    "/orders/complete"
)
async def post_complete():
    return 'pong'

