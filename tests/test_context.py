import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app

# app = FastAPI()

client = TestClient(app)


def test_read_main():
    test_str = "Hello!"
    response = client.get("/", headers={"X-Request_ID": test_str})
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
    print(type(response.headers["x-context"]))
    assert json.loads(response.headers["x-context"])["X-Request-ID"] == test_str
