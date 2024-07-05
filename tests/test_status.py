from fastapi.testclient import TestClient 
from fastapi_tema.main import app
from fastapi_tema.settings import Settings_my

def test_client_status():
    client = TestClient(app)
    result = client.get(Settings_my.main_url)
    assert result.status_code == 200