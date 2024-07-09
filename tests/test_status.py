from fastapi.testclient import TestClient 
from fastapi_tema.aplication.main import app
from fastapi_tema.aplication.settings import settings

def test_client_status():
    client = TestClient(app)
    result = client.get(settings.main_url)
    assert result.status_code == 200
