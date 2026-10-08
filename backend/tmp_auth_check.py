from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
resp = client.post('/api/auth/register', json={'email':'direct-check@example.com','full_name':'Direct Check','password':'securepassword123'})
print(resp.status_code)
print(resp.text)
