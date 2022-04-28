from datetime import datetime,timedelta
import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.tests.db_utils import setup_db, close_connection


@pytest.fixture
async def test_db():
    await setup_db()
    await close_connection()
    yield

@pytest.mark.asyncio
async def test_message_group(test_db):
    with TestClient(app) as client:
        args = {
            'chat_id': 123,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/?chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        result = response.json()['messages']
        assert result[0]['body'] == 'message1'
        assert result[0]['tg_id'] == 123
        assert result[1]['body'] == 'message2'
        assert result[1]['tg_id'] == 123
        assert result[2]['body'] == 'message3'
        assert result[2]['tg_id'] == 125
        args = {
            'chat_id': 123,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now()-timedelta(days=1))
        }
        response = client.get(f'/message/group/?chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        result = response.json()['messages']
        assert result[0]['body'] == 'message2'
        assert result[0]['tg_id'] == 123
        args = {
            'chat_id': 123,
            'start_date': str(datetime.now()),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/?chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        result = response.json()['messages']
        assert len(result) == 0
        args = {
            'chat_id': 126,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/?chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        result = response.json()['messages']
        assert len(result) == 0
        args = {
            'chat_id': 124,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/?chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        result = response.json()['messages']
        assert result[0]['tg_id'] == 124
        assert result[0]['body'] == 'message4'


@pytest.mark.asyncio
async def test_message_group_user(test_db):
    with TestClient(app) as client:
        args = {
            'tg_id': 123,
            'chat_id': 123,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/user?tg_id={args["tg_id"]}&'
                              f'chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        result = response.json()['messages']
        assert len(result) == 2
        assert result[0]['body'] == 'message1'
        assert result[1]['body'] == 'message2'
        args = {
            'tg_id': 124,
            'chat_id': 124,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/user?tg_id={args["tg_id"]}&'
                              f'chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        result = response.json()['messages']
        assert len(result) == 1
        assert result[0]['body'] == 'message4'

        args = {
            'tg_id': 123,
            'chat_id': 123,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now()-timedelta(days=1))
        }
        response = client.get(f'/message/group/user?tg_id={args["tg_id"]}&'
                              f'chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        result = response.json()['messages']
        assert len(result) == 1
        assert result[0]['body'] == 'message2'
        args = {
            'tg_id': 126,
            'chat_id': 123,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/user?tg_id={args["tg_id"]}&'
                              f'chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        result = response.json()['messages']
        assert len(result) == 0
        args = {
            'tg_id': 123,
            'chat_id': 126,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/user?tg_id={args["tg_id"]}&'
                              f'chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        result = response.json()['messages']
        assert len(result) == 0

@pytest.mark.asyncio
async def test_message_group_count(test_db):
    with TestClient(app) as client:
        args = {
            'chat_id': 123,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/count?chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        assert response.json() == 3
        args = {
            'chat_id': 123,
            'start_date': str(datetime.now()),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/count?chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        assert response.json() == 0
        args = {
            'chat_id': 123,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now()-timedelta(days=1))
        }
        response = client.get(f'/message/group/count?chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        assert response.json() == 1
        args = {
            'chat_id': 126,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/count?chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        assert response.json() == 0

@pytest.mark.asyncio
async def test_message_group_user_count(test_db):
    with TestClient(app) as client:
        args = {
            'tg_id': 123,
            'chat_id': 123,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/user/count?tg_id={args["tg_id"]}&'
                              f'chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        assert response.json() == 2
        args = {
            'tg_id': 123,
            'chat_id': 123,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now()-timedelta(days=1))
        }
        response = client.get(f'/message/group/user/count?tg_id={args["tg_id"]}&'
                              f'chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        assert response.json() == 1
        args = {
            'tg_id': 124,
            'chat_id': 124,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/user/count?tg_id={args["tg_id"]}&'
                              f'chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        assert response.json() == 1
        args = {
            'tg_id': 123,
            'chat_id': 123,
            'start_date': str(datetime.now()),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/user/count?tg_id={args["tg_id"]}&'
                              f'chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        assert response.json() == 0
        args = {
            'tg_id': 126,
            'chat_id': 123,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/user/count?tg_id={args["tg_id"]}&'
                              f'chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        assert response.json() == 0
        args = {
            'tg_id': 123,
            'chat_id': 126,
            'start_date': str(datetime.now()-timedelta(days=2)),
            'end_date': str(datetime.now())
        }
        response = client.get(f'/message/group/user/count?tg_id={args["tg_id"]}&'
                              f'chat_id={args["chat_id"]}&'
                              f'start_date={args["start_date"]}&'
                              f'end_date={args["end_date"]}')
        assert response.status_code == 200
        assert response.json() == 0


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
        response = client.get(f'/message/group/count?chat_id={123}&'
                              f'start_date={str(datetime.now()-timedelta(days=2))}&'
                              f'end_date={str(datetime.now())}')
        assert response.status_code == 200
        assert response.json() == 4
