"""Integration tests for app.py"""
import pytest
import json

from bank_api.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_account_creation(client):
    response_post = client.post('/accounts/test')
    response_get = client.get('/accounts/test')
    
    data_get = json.loads(response_post.data)
    data_post = json.loads(response_get.data)

    assert response_get.status_code == 200
    assert response_post.status_code == 200
    assert data_get['name'] == 'test'
    assert data_post['name'] == 'test'
    

def test_get_nonexistant_account_fails404(client):
    response_get = client.get('/accounts/nonexistant')

    assert response_get.status_code == 404
    

def test_account_balance(client):
    client.post('/accounts/test')
    response_before = client.get('/accounts/test')
    client.post('/money', data={
        'name': 'test',
        'amount': 100
    })
    response_after = client.get('/accounts/test')

    data_before = json.loads(response_before.data)
    data_after = json.loads(response_after.data)

    assert response_before.status_code == 200
    assert response_after.status_code == 200
    assert data_before['name'] == 'test'
    assert data_after['name'] == 'test'
    assert data_before['amount'] == 0
    assert data_after['amount'] == 100


def test_move_funds(client):
    client.post('/accounts/AccountFrom')
    client.post('/accounts/AccountTo')
    response_move = client.post('/money/move', data={
        'nameFrom': 'AccountFrom',
        'nameTo': 'AccountTo',
        'amount': 20
    })
    account_from = json.loads(client.get('/accounts/AccountFrom').data)
    account_to = json.loads(client.get('/accounts/AccountTo').data)

    assert account_from['amount'] == -20
    assert account_to['amount'] == 20
    assert response_move.status_code == 200