import unittest
import uuid
from fastapi.testclient import TestClient
from app.main import app

class RoadmapIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        # Register and login candidate 1
        uid = str(uuid.uuid4())[:8]
        self.email = f"roadmap_user_{uid}@example.com"
        self.password = "securepass123"
        self.client.post("/api/auth/register", json={
            "email": self.email,
            "full_name": f"Roadmap Student {uid}",
            "password": self.password
        })
        login_res = self.client.post("/api/auth/token", json={
            "email": self.email,
            "password": self.password
        })
        self.token = login_res.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_roadmap_lifecycle_end_to_end(self) -> None:
        # 1. Unauthenticated request should fail with 401
        unauth_resp = self.client.get("/api/roadmap/me")
        self.assertEqual(unauth_resp.status_code, 401)

        # 2. Before onboarding, request should return 404
        pre_onboard_resp = self.client.get("/api/roadmap/me", headers=self.headers)
        self.assertEqual(pre_onboard_resp.status_code, 404)

        # 3. Complete onboarding
        onboarding_payload = {
            "user_type": "College Student",
            "career_goal": "Product Company Placement",
            "company_type": "Product-based",
            "dream_company": "Google",
            "target_role": "Software Engineer",
            "current_level": "Intermediate",
            "skills": ["Python", "Data Structures", "Algorithms"]
        }
        onboard_res = self.client.post("/api/onboarding/", json=onboarding_payload, headers=self.headers)
        self.assertEqual(onboard_res.status_code, 200, onboard_res.text)

        # 4. Fetch roadmap after onboarding -> automatically generated!
        roadmap_resp = self.client.get("/api/roadmap/me", headers=self.headers)
        self.assertEqual(roadmap_resp.status_code, 200, roadmap_resp.text)
        roadmap_data = roadmap_resp.json()

        self.assertIn("roadmap_id", roadmap_data)
        self.assertEqual(roadmap_data["target_company"], "Google")
        self.assertEqual(roadmap_data["target_role"], "Software Engineer")
        self.assertIn("Google", roadmap_data["title"])
        self.assertGreater(len(roadmap_data["tasks"]), 0)
        self.assertGreater(len(roadmap_data["skill_gaps"]), 0)
        self.assertGreater(len(roadmap_data["company_recommendations"]), 0)

        tasks = roadmap_data["tasks"]
        first_task = tasks[0]
        self.assertFalse(first_task["completed"])
        self.assertIn("priority", first_task)
        self.assertIn("due_date", first_task)

        progress = roadmap_data["progress"]
        self.assertEqual(progress["completed_count"], 0)
        self.assertEqual(progress["completion_percentage"], 0.0)
        self.assertEqual(progress["xp_points"], 0)
        self.assertEqual(progress["total_tasks"], len(tasks))

        # 5. Toggle task completion (Mark as completed)
        toggle_resp = self.client.patch(f"/api/roadmap/tasks/{first_task['id']}/toggle", headers=self.headers)
        self.assertEqual(toggle_resp.status_code, 200, toggle_resp.text)
        toggle_data = toggle_resp.json()
        self.assertTrue(toggle_data["completed"])
        self.assertEqual(toggle_data["progress"]["completed_count"], 1)
        self.assertGreater(toggle_data["progress"]["completion_percentage"], 0)
        self.assertEqual(toggle_data["progress"]["xp_points"], 50)

        # 6. Verify GET /api/roadmap/me reflects the completed task
        roadmap_updated = self.client.get("/api/roadmap/me", headers=self.headers).json()
        self.assertEqual(roadmap_updated["progress"]["completed_count"], 1)
        self.assertEqual(roadmap_updated["progress"]["xp_points"], 50)
        updated_first_task = next(t for t in roadmap_updated["tasks"] if t["id"] == first_task["id"])
        self.assertTrue(updated_first_task["completed"])

        # 7. Toggle task back to incomplete
        toggle_back_resp = self.client.patch(f"/api/roadmap/tasks/{first_task['id']}/toggle", headers=self.headers)
        self.assertEqual(toggle_back_resp.status_code, 200)
        self.assertFalse(toggle_back_resp.json()["completed"])
        self.assertEqual(toggle_back_resp.json()["progress"]["completed_count"], 0)
        self.assertEqual(toggle_back_resp.json()["progress"]["xp_points"], 0)

        # 8. Test standalone endpoints: /skill-gaps and /progress
        gaps_resp = self.client.get("/api/roadmap/skill-gaps", headers=self.headers)
        self.assertEqual(gaps_resp.status_code, 200)
        self.assertGreater(len(gaps_resp.json()), 0)

        prog_resp = self.client.get("/api/roadmap/progress", headers=self.headers)
        self.assertEqual(prog_resp.status_code, 200)
        self.assertEqual(prog_resp.json()["completed_count"], 0)

        # 9. Force regenerate roadmap
        regen_resp = self.client.post("/api/roadmap/generate", headers=self.headers)
        self.assertEqual(regen_resp.status_code, 200)
        self.assertIn("roadmap_id", regen_resp.json())

        # 10. Authorization protection: User 2 cannot toggle User 1's task
        uid2 = str(uuid.uuid4())[:8]
        self.client.post("/api/auth/register", json={
            "email": f"user2_{uid2}@example.com",
            "password": "user2pass123",
            "full_name": f"User Two {uid2}"
        })
        login2 = self.client.post("/api/auth/token", json={
            "email": f"user2_{uid2}@example.com",
            "password": "user2pass123"
        })
        headers2 = {"Authorization": f"Bearer {login2.json()['access_token']}"}

        user1_latest_tasks = self.client.get("/api/roadmap/me", headers=self.headers).json()["tasks"]
        target_task_id = user1_latest_tasks[0]["id"]

        cross_toggle_resp = self.client.patch(f"/api/roadmap/tasks/{target_task_id}/toggle", headers=headers2)
        self.assertEqual(cross_toggle_resp.status_code, 403)

    def test_company_specific_roadmaps(self) -> None:
        companies = ["Amazon", "Zoho", "TCS", "Infosys", "Microsoft"]
        for comp in companies:
            uid = str(uuid.uuid4())[:8]
            email = f"student_{comp.lower()}_{uid}@example.com"
            self.client.post("/api/auth/register", json={
                "email": email,
                "full_name": f"{comp} Student {uid}",
                "password": "password123"
            })
            login = self.client.post("/api/auth/token", json={
                "email": email,
                "password": "password123"
            })
            headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

            self.client.post("/api/onboarding/", json={
                "user_type": "College Student",
                "career_goal": "Placement",
                "company_type": "Product-based" if comp in ["Amazon", "Zoho", "Microsoft"] else "Service-based",
                "dream_company": comp,
                "target_role": "Software Developer",
                "current_level": "Intermediate",
                "skills": ["Java", "DSA"]
            }, headers=headers)

            roadmap = self.client.get("/api/roadmap/me", headers=headers).json()
            self.assertEqual(roadmap["target_company"], comp)
            self.assertIn(comp, roadmap["title"])
            self.assertGreater(len(roadmap["company_recommendations"]), 0)
            self.assertGreater(len(roadmap["tasks"]), 0)

    def test_mock_interview_booster_task_generation(self) -> None:
        uid = str(uuid.uuid4())[:8]
        email = f"interview_booster_{uid}@example.com"
        self.client.post("/api/auth/register", json={
            "email": email,
            "full_name": f"Booster Student {uid}",
            "password": "password123"
        })
        login = self.client.post("/api/auth/token", json={
            "email": email,
            "password": "password123"
        })
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        self.client.post("/api/onboarding/", json={
            "user_type": "College Student",
            "career_goal": "Placement",
            "company_type": "Product-based",
            "dream_company": "Amazon",
            "target_role": "Software Engineer",
            "current_level": "Intermediate",
            "skills": ["Python", "DSA"]
        }, headers=headers)

        # Start an interview session
        session_resp = self.client.post("/api/interview/sessions", json={
            "company_name": "Amazon",
            "role": "Software Engineer",
            "difficulty": "Medium"
        }, headers=headers)
        self.assertEqual(session_resp.status_code, 200, session_resp.text)
        session_id = session_resp.json()["id"]
        q_id = session_resp.json()["questions"][0]["id"]

        # Submit answer and complete session
        self.client.post(f"/api/interview/questions/{q_id}/answer", json={
            "response": "I would use a priority queue min-heap to solve this in O(N log K)."
        }, headers=headers)
        self.client.post(f"/api/interview/sessions/{session_id}/complete", headers=headers)

        # Regenerate roadmap
        regen = self.client.post("/api/roadmap/generate", headers=headers).json()
        task_titles = [t["title"] for t in regen["tasks"]]
        self.assertTrue(any("Post-Interview" in t or "Weak Area" in t for t in task_titles))


if __name__ == "__main__":
    unittest.main()

