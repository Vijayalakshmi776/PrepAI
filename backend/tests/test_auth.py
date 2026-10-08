import unittest
import uuid

from fastapi.testclient import TestClient

from app.main import app


class AuthEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_duplicate_registration_returns_conflict(self) -> None:
        email = f"duplicate-{uuid.uuid4()}@example.com"
        payload = {
            "email": email,
            "full_name": "Duplicate User",
            "password": "securepassword123",
        }

        first_response = self.client.post("/api/auth/register", json=payload)
        self.assertEqual(first_response.status_code, 201)

        second_response = self.client.post("/api/auth/register", json=payload)
        self.assertEqual(second_response.status_code, 409)


if __name__ == "__main__":
    unittest.main()
