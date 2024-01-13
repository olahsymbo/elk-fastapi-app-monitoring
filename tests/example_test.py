import uuid
import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from apps.app import app

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_create_user(test_db):
    response = client.post("/create_user/") 
    assert response.status_code == 200 

def test_get_user(test_db):
    response = client.get("/get_user/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User found"
    assert response.json()["errors"] == None
    assert response.json()['data']['id'] == 1

def test_get_user_incorrect(test_db):
    response = client.get("/get_user/2000")
    assert response.status_code == 404
    assert response.json()["message"] == "User not found"
    assert response.json()["errors"] == None

def test_update_user(test_db): 
    name = str(uuid.uuid4())
    payload = json.dumps({
        "name": name,
        "email": f"{name}@email.com"
        })
    response = client.put("/update_user/1", headers={}, data=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"
    assert response.json()["errors"] == None