import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api import app
from app.migrations.db import DB
from app.tests.db_utils import setup_db, close_connection

client = TestClient(app)

@pytest_asyncio.fixture
async def test_db():
    await setup_db()
    yield
    await close_connection()

@pytest.mark.asyncio
def test_add(test_db):
    response = client.get('/')
    assert response.status_code == 200
