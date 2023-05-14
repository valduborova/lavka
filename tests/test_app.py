import pytest
import json
from fastapi.testclient import TestClient


def test_clear_db_begin(client: TestClient):
    response = client.get("/clear_db")
    assert response.status_code == 200


def test_post_couriers_id_conflict_1(client: TestClient):
    couriers = [
        {"courier_id": 1, "region": 1, "type_id": "foot",
            "working_graphics": ["09:00-11:00"]},
        {"courier_id": 1, "region": 2, "type_id": "bike",
            "working_graphics": ["09:00-18:00", "20:00-22:00"]}
    ]
    headers = {"Content-Type": "application/json"}
    response = client.post("/couriers", json=couriers, headers=headers)
    assert response.status_code == 400
    assert response.json() == {
        "message": "courier_id already exists", "courier_id": 1}


def test_post_couriers(client: TestClient):
    couriers = [
        {"courier_id": 1, "region": 1, "type_id": "foot",
            "working_graphics": ["09:00-11:00"]},
        {"courier_id": 2, "region": 2, "type_id": "bike",
            "working_graphics": ["09:00-18:00", "20:00-22:00"]},
        {"courier_id": 3, "region": 3, "type_id": "car",
            "working_graphics": ["09:00-18:00", "20:00-22:00"]},
    ]
    headers = {"Content-Type": "application/json"}
    response = client.post("/couriers", json=couriers, headers=headers)
    assert response.status_code == 200


def test_post_couriers_id_conflict_2(client: TestClient):
    couriers = [
        {"courier_id": 1, "region": 1, "type_id": "foot",
            "working_graphics": ["09:00-11:00"]}
    ]
    headers = {"Content-Type": "application/json"}
    response = client.post("/couriers", json=couriers, headers=headers)
    assert response.status_code == 400
    assert response.json() == {
        "message": "courier_id already exists", "courier_id": 1}


def test_post_couriers_validation_error_1(client: TestClient):
    couriers = [
        {"courier_id": "a", "region": 1, "type_id": "foot",
            "working_graphics": ["09:00-11:00"]}
    ]
    headers = {"Content-Type": "application/json"}
    response = client.post("/couriers", json=couriers, headers=headers)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'body', 0, 'courier_id'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}


def test_post_couriers_validation_error_2(client: TestClient):
    couriers = [
        {"courier_id": 1, "region": "a", "type_id": "foot",
            "working_graphics": ["09:00-11:00"]}
    ]
    headers = {"Content-Type": "application/json"}
    response = client.post("/couriers", json=couriers, headers=headers)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'body', 0, 'region'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}


def test_post_couriers_validation_error_3(client: TestClient):
    couriers = [
        {"courier_id": 1, "region": 1, "type_id": "leg",
            "working_graphics": ["09:00-11:00"]}
    ]
    headers = {"Content-Type": "application/json"}
    response = client.post("/couriers", json=couriers, headers=headers)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 0, 'type_id'], 'msg': "value is not a valid enumeration member; permitted: 'foot', 'bike', 'car'",
                                           'type': 'type_error.enum', 'ctx': {'enum_values': ['foot', 'bike', 'car']}}]}


def test_post_couriers_validation_error_4(client: TestClient):
    couriers = [
        {"courier_id": 1, "region": 1, "type_id": "foot",
            "working_graphics": ["09:00-11:00", "09:00-11:61"]}
    ]
    headers = {"Content-Type": "application/json"}
    response = client.post("/couriers", json=couriers, headers=headers)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 0, 'working_graphics', 1], 'msg': 'string does not match regex "^([01][0-9]|2[0-3]):[0-5][0-9]-([01][0-9]|2[0-3]):[0-5][0-9]$"',
                                           'type': 'value_error.str.regex', 'ctx': {'pattern': '^([01][0-9]|2[0-3]):[0-5][0-9]-([01][0-9]|2[0-3]):[0-5][0-9]$'}}]}


def test_clear_db_end_1(client: TestClient):
    response = client.get("/clear_db")
    assert response.status_code == 200


def test_meta_info_validation_1(client: TestClient):
    payload = {"start_date": "2021-01-01", "end_date": "2023-01-01"}
    response = client.get("/couriers/meta-info/a", params=payload)
    assert response.status_code == 422


def test_meta_info_validation_2(client: TestClient):
    payload = {"start_date": "2023-01-01", "end_date": "2021-01-01"}
    response = client.get("/couriers/meta-info/1", params=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "start_date must be earlier than end_date"}


def test_meta_info_1(client: TestClient):
    payload = {"start_date": "2021-01-01", "end_date": "2023-01-01"}
    response = client.get("/couriers/meta-info/1", params=payload)
    assert response.status_code == 404
    assert response.json() == {"message": "Provided courier_id=1 not found"}


def test_meta_info_2(client: TestClient):
    couriers = [
        {"courier_id": 1, "region": 1, "type_id": "foot",
            "working_graphics": ["09:00-11:00"]},
        {"courier_id": 2, "region": 2, "type_id": "bike",
            "working_graphics": ["09:00-18:00", "20:00-22:00"]},
        {"courier_id": 3, "region": 3, "type_id": "car",
            "working_graphics": ["09:00-18:00", "20:00-22:00"]}
    ]
    headers = {"Content-Type": "application/json"}
    response = client.post("/couriers", json=couriers, headers=headers)
    assert response.status_code == 200
    payload = {"start_date": "2021-01-01", "end_date": "2023-01-01"}
    response = client.get("/couriers/meta-info/1", params=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Provided courier_id=1 does not have any orders in provided time period"}


def test_meta_info_3(client: TestClient):
    orders = [
        {"order_id": 1, "weight": 0.23, "region": 1, "ordered_at": "2021-01-10T10:31:01.42Z", "delivery_price": 100},
        {"order_id": 2, "weight": 15, "region": 1, "ordered_at": "2021-01-10T10:31:01.42Z", "delivery_price": 100},
        {"order_id": 3, "weight": 0.01, "region": 1, "ordered_at": "2021-01-10T10:31:01.42Z", "delivery_price": 100},
    ]
    response = client.post("/orders", json=orders)
    assert response.status_code == 200
    completions = [
        {"courier_id": 1, "order_id": 1, "delivered_at": "2021-01-10T10:33:01.42Z"},
        {"courier_id": 1, "order_id": 2, "delivered_at": "2021-01-10T10:33:01.42Z"},
        {"courier_id": 1, "order_id": 3, "delivered_at": "2021-01-10T10:33:01.42Z"},
    ]
    for completion in completions:
        response = client.post("/orders/complete", json=completion)
        assert response.status_code == 200
    payload = {"start_date": "2021-01-10", "end_date": "2021-01-11"}
    response = client.get("/couriers/meta-info/1", params=payload)
    assert response.status_code == 200
    assert response.json() == {'income': 600.0, 'rating': 0.375}