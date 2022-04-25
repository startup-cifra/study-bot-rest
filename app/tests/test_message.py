from datetime import datetime,timedelta
import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api import app
from app.migrations.db import DB
from app.tests.db_utils import setup_db, close_connection


@pytest.fixture
async def test_db():
    await setup_db()
    await close_connection()
    yield

@pytest.mark.asyncio
async def test_add(test_db):
    with TestClient(app) as client: 
        response = client.post('/message',json={
            'tg_id':0,
            'chat_id':0,
            'body':'string',
            'date': str(datetime.now())
        })
        assert response.status_code == 422
        response = client.post('/message',json={
            'tg_id':123,
            'chat_id':123,
            'body':'string',
            'date': str(datetime.now())
        })
        assert response.status_code == 201
        response = client.post('/message',json={
            'tg_id':123,
            'chat_id':124,
            'body':'string',
            'date': str(datetime.now())
        })
        assert response.status_code == 400
        response = client.post('/message',json={
            'tg_id':127,
            'chat_id':129,
            'body':'string',
            'date': str(datetime.now())
        })
        assert response.status_code == 400
        response = client.post('/message',json={
            'tg_id':123,
            'chat_id':123,
        })
        assert response.status_code == 422
        response = client.get(f'/message/group/count?chat_id={123}&start_date={str(datetime.now()-timedelta(days=2))}&end_date={str(datetime.now())}')
        assert response.status_code == 200
        assert response.json() == 4
    
