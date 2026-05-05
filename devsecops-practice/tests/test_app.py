from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_secret_unauthorized() -> None:
    response = client.post('/api/secret', json={'username': 'alice', 'environment': 'dev'})
    assert response.status_code == 401


def test_secret_authorized() -> None:
    response = client.post(
        '/api/secret',
        headers={'x-api-key': 'change-me-in-prod'},
        json={'username': 'alice', 'environment': 'dev'},
    )
    assert response.status_code == 200
