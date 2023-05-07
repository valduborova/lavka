from fastapi import APIRouter, Request
from starlette import status
from pydantic import BaseModel
# import json

router = APIRouter()


class Item(BaseModel):
    name: str


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
async def post_couriers(item: Item):
    return item.name


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

