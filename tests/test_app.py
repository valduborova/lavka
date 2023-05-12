import pytest
from fastapi.testclient import TestClient


def test_clear_db_begin(client: TestClient):
    response = client.get("/clear_db")
    assert response.status_code == 200


def test_ping(client: TestClient):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json() == 'pong'


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
            "working_graphics": ["09:00-18:00", "20:00-22:00"]}
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


def test_clear_db_end(client: TestClient):
    response = client.get("/clear_db")
    assert response.status_code == 200

#! примерно в этом месте ratelimit начнет работать и выбивать 429 ошибку
