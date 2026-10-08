import unittest
import uuid
from fastapi.testclient import TestClient
from app.main import app

class IntegrationFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_full_register_login_onboarding_flow(self) -> None:
        # 1. Register
        unique_id = str(uuid.uuid4())[:8]
        email = f"student_{unique_id}@example.com"
        full_name = f"Test Student {unique_id}"
        password = "strongpassword123"

        reg_resp = self.client.post("/api/auth/register", json={
            "email": email,
            "full_name": full_name,
            "password": password
        })
        self.assertEqual(reg_resp.status_code, 201, reg_resp.text)
        reg_data = reg_resp.json()
        self.assertEqual(reg_data["email"], email)
        self.assertEqual(reg_data["full_name"], full_name)

        # 2. Login to /api/auth/token
        login_resp = self.client.post("/api/auth/token", json={
            "email": email,
            "password": password
        })
        self.assertEqual(login_resp.status_code, 200, login_resp.text)
        token_data = login_resp.json()
        self.assertIn("access_token", token_data)
        self.assertEqual(token_data["token_type"], "bearer")
        token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Verify /api/auth/me with JWT
        me_resp = self.client.get("/api/auth/me", headers=headers)
        self.assertEqual(me_resp.status_code, 200, me_resp.text)
        me_data = me_resp.json()
        self.assertEqual(me_data["email"], email)

        # 4. Check profile before onboarding -> 404
        profile_pre_resp = self.client.get("/api/onboarding/me", headers=headers)
        self.assertEqual(profile_pre_resp.status_code, 404)

        # 5. Submit Onboarding data
        onboarding_payload = {
            "user_type": "College Student",
            "career_goal": "Placement",
            "company_type": "Product-based",
            "dream_company": "Google",
            "target_role": "Software Engineer",
            "current_level": "Intermediate",
            "skills": ["Python", "Data Structures", "SQL"]
        }
        onboard_resp = self.client.post("/api/onboarding/", json=onboarding_payload, headers=headers)
        self.assertEqual(onboard_resp.status_code, 200, onboard_resp.text)
        onboard_data = onboard_resp.json()
        self.assertEqual(onboard_data["status"], "ok")
        self.assertIsNotNone(onboard_data.get("profile_id"))

        # 6. Retrieve profile after onboarding -> 200 with saved values
        profile_post_resp = self.client.get("/api/onboarding/me", headers=headers)
        self.assertEqual(profile_post_resp.status_code, 200, profile_post_resp.text)
        profile_data = profile_post_resp.json()
        self.assertEqual(profile_data["target_company"], "Google")
        self.assertEqual(profile_data["target_role"], "Software Engineer")
        self.assertEqual(profile_data["current_level"], "Intermediate")
        self.assertEqual(profile_data["career_goal"], "Placement")

if __name__ == "__main__":
    unittest.main()
