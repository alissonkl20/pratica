import pytest
import json
from app import app
from sqlar import db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            pass

def test_create_tarefa(client):
    response = client.post('/tarefas', json={
        'titulo': 'Teste',
        'descricao': 'Descrição teste'
    })
    assert response.status_code == 201
    assert 'Tarefa criada com sucesso' in response.get_json()['message']

def test_create_tarefa_empty_title(client):
    response = client.post('/tarefas', json={
        'titulo': '',
        'descricao': 'Descrição teste'
    })
    assert response.status_code == 400

def test_get_tarefas(client):
    response = client.get('/tarefas')
    assert response.status_code == 200
    assert 'tarefas' in response.get_json()