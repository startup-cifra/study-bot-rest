import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api import app
from app.migrations.db import DB

client = TestClient(app)


def test_add():
    response = client.get('/')
    assert response.status_code == 200
