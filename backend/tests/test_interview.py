import re
import unittest
import uuid
from fastapi.testclient import TestClient
from app.main import app

class MockInterviewIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from app.core.config import settings
        cls._orig_key = settings.GEMINI_API_KEY
        settings.GEMINI_API_KEY = ""

    @classmethod
    def tearDownClass(cls):
        from app.core.config import settings
        settings.GEMINI_API_KEY = cls._orig_key

    def setUp(self) -> None:
        self.client = TestClient(app)
        # Register and log in a fresh user
        uid = str(uuid.uuid4())[:8]
        self.email = f"candidate_{uid}@example.com"
        self.password = "interviewpass123"
        self.client.post("/api/auth/register", json={
            "email": self.email,
            "full_name": f"Candidate {uid}",
            "password": self.password
        })
        login_res = self.client.post("/api/auth/token", json={
            "email": self.email,
            "password": self.password
        })
        self.token = login_res.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_mock_interview_full_flow(self) -> None:
        # 1. Fetch companies catalog
        comp_res = self.client.get("/api/interview/companies")
        self.assertEqual(comp_res.status_code, 200, comp_res.text)
        companies = comp_res.json()
        self.assertGreater(len(companies), 0)
        tcs_company = next((c for c in companies if c["name"] == "TCS"), companies[0])
        self.assertIn("patterns", tcs_company)
        self.assertGreater(len(tcs_company["patterns"]), 0)
        
        # Round 1 is Aptitude
        round_1 = tcs_company["patterns"][0]["rounds"][0]

        # 2. Start mock interview session
        session_payload = {
            "company_name": tcs_company["name"],
            "role": "Software Engineer",
            "difficulty": "Medium",
            "round_title": round_1["title"],
            "round_id": round_1["id"],
            "company_id": tcs_company["id"]
        }
        start_res = self.client.post("/api/interview/sessions", json=session_payload, headers=self.headers)
        self.assertEqual(start_res.status_code, 200, start_res.text)
        session_data = start_res.json()
        session_id = session_data["id"]
        
        # Verify first round is Aptitude
        current_round = session_data.get("current_round")
        self.assertIsNotNone(current_round)
        self.assertIn("Aptitude", current_round["title"])
        
        questions = session_data["questions"]
        self.assertEqual(len(questions), 10)

        # 3. Retrieve session details
        get_res = self.client.get(f"/api/interview/sessions/{session_id}", headers=self.headers)
        self.assertEqual(get_res.status_code, 200, get_res.text)
        self.assertFalse(get_res.json()["completed"])

        # 4. Complete Aptitude round
        for i, q in enumerate(questions):
            ans_text = q["options"][0] if (q.get("options") and len(q["options"]) > 0) else "Sample response"
            ans_res = self.client.post(
                f"/api/interview/questions/{q['id']}/answer",
                json={"response": ans_text},
                headers=self.headers
            )
            self.assertEqual(ans_res.status_code, 200, ans_res.text)
            ans_data = ans_res.json()
            self.assertIn("score", ans_data)
            self.assertIn("feedback", ans_data)
            self.assertIn(ans_data["score"], [0, 100])

        # 5. Complete interview session
        comp_res = self.client.post(f"/api/interview/sessions/{session_id}/complete", headers=self.headers)
        self.assertEqual(comp_res.status_code, 200, comp_res.text)
        comp_data = comp_res.json()
        self.assertTrue(comp_data["completed"])
        
        # 6. Verify final feedback
        self.assertIn("summary", comp_data)
        self.assertIn("strengths", comp_data)
        self.assertIn("weaknesses", comp_data)
        self.assertIn("recommendations", comp_data)

    def test_consecutive_sessions_produce_different_aptitude_sets(self) -> None:
        """Requirement 1 & 6: Verify two consecutive sessions produce different aptitude question sets."""
        payload = {
            "company_name": "TCS",
            "role": "Software Engineer",
            "difficulty": "Medium",
            "round_title": "Round 1: Aptitude"
        }
        res1 = self.client.post("/api/interview/sessions", json=payload, headers=self.headers)
        self.assertEqual(res1.status_code, 200, res1.text)
        s1_questions = [q["prompt"] for q in res1.json()["questions"]]

        res2 = self.client.post("/api/interview/sessions", json=payload, headers=self.headers)
        self.assertEqual(res2.status_code, 200, res2.text)
        s2_questions = [q["prompt"] for q in res2.json()["questions"]]

        # Consecutive sessions must not have identical question ordering/subsets
        self.assertNotEqual(s1_questions, s2_questions, "Consecutive sessions produced identical aptitude sets!")

    def test_no_duplicate_questions_within_session(self) -> None:
        """Requirement 1 & 6: Prevent duplicate questions within the same interview session."""
        payload = {
            "company_name": "Infosys",
            "role": "Software Engineer",
            "difficulty": "Medium",
            "round_title": "Round 1: Aptitude"
        }
        res = self.client.post("/api/interview/sessions", json=payload, headers=self.headers)
        self.assertEqual(res.status_code, 200, res.text)
        questions = res.json()["questions"]
        prompts = [q["prompt"] for q in questions]

        self.assertEqual(len(prompts), len(set(prompts)), "Duplicate questions found within the same session!")

    def test_company_specific_question_pools(self) -> None:
        """Requirement 2 & 6: TCS, Infosys, Zoho, Google, Amazon, Microsoft, Startup must use separate practice question pools."""
        companies = ["TCS", "Infosys", "Zoho", "Google", "Amazon", "Microsoft", "Startup"]
        prompts_by_company = {}

        for company in companies:
            payload = {
                "company_name": company,
                "role": "Software Engineer",
                "difficulty": "Medium",
                "round_title": "Round 1: Aptitude"
            }
            res = self.client.post("/api/interview/sessions", json=payload, headers=self.headers)
            self.assertEqual(res.status_code, 200, res.text)
            prompts_by_company[company] = set(q["prompt"] for q in res.json()["questions"])

        # Compare Google vs TCS vs Zoho vs Startup - their specific pools must differ
        self.assertNotEqual(prompts_by_company["Google"], prompts_by_company["TCS"])
        self.assertNotEqual(prompts_by_company["Zoho"], prompts_by_company["Infosys"])
        self.assertNotEqual(prompts_by_company["Amazon"], prompts_by_company["Microsoft"])
        self.assertNotEqual(prompts_by_company["Startup"], prompts_by_company["Google"])

    def test_one_question_at_a_time_flow_and_answer_persistence(self) -> None:
        """Requirement 3, 5 & 6: Test one-question-at-a-time answer submission and persistence."""
        payload = {
            "company_name": "Zoho",
            "role": "Software Engineer",
            "difficulty": "Medium",
            "round_title": "Round 1: Aptitude"
        }
        res = self.client.post("/api/interview/sessions", json=payload, headers=self.headers)
        self.assertEqual(res.status_code, 200, res.text)
        session = res.json()
        questions = session["questions"]

        # Submit answer for Question 1
        q1 = questions[0]
        selected_option = q1["options"][0] if q1.get("options") else "Answer 1"
        ans_res1 = self.client.post(
            f"/api/interview/questions/{q1['id']}/answer",
            json={"response": selected_option},
            headers=self.headers
        )
        self.assertEqual(ans_res1.status_code, 200, ans_res1.text)
        ans_data1 = ans_res1.json()
        self.assertEqual(ans_data1["response"], selected_option)

        # Submit answer for Question 2
        q2 = questions[1]
        selected_option2 = q2["options"][1] if q2.get("options") and len(q2["options"]) > 1 else "Answer 2"
        ans_res2 = self.client.post(
            f"/api/interview/questions/{q2['id']}/answer",
            json={"response": selected_option2},
            headers=self.headers
        )
        self.assertEqual(ans_res2.status_code, 200, ans_res2.text)
        ans_data2 = ans_res2.json()
        self.assertEqual(ans_data2["response"], selected_option2)

    def test_session_persistence_after_refresh(self) -> None:
        """Requirement 4 & 6: Fetching an existing session restores answers and state (simulating page refresh)."""
        payload = {
            "company_name": "Amazon",
            "role": "Software Engineer",
            "difficulty": "Medium",
            "round_title": "Round 1: Aptitude"
        }
        start_res = self.client.post("/api/interview/sessions", json=payload, headers=self.headers)
        self.assertEqual(start_res.status_code, 200, start_res.text)
        session_id = start_res.json()["id"]
        q1 = start_res.json()["questions"][0]

        # Submit answer to Q1
        opt = q1["options"][0] if q1.get("options") else "Sample Option"
        self.client.post(
            f"/api/interview/questions/{q1['id']}/answer",
            json={"response": opt},
            headers=self.headers
        )

        # Simulate page refresh by fetching session again via GET endpoint
        get_res = self.client.get(f"/api/interview/sessions/{session_id}", headers=self.headers)
        self.assertEqual(get_res.status_code, 200, get_res.text)
        refreshed_session = get_res.json()

        self.assertEqual(refreshed_session["id"], session_id)
        self.assertFalse(refreshed_session["completed"])
        
        # Verify answer was persisted
        q1_refreshed = next(q for q in refreshed_session["questions"] if q["id"] == q1["id"])
        self.assertIsNotNone(q1_refreshed["answer"])
        self.assertEqual(q1_refreshed["answer"]["response"], opt)

    def test_final_evaluation_preservation(self) -> None:
        """Requirement 5 & 6: Verify final score and feedback are preserved after session completion."""
        payload = {
            "company_name": "Microsoft",
            "role": "Software Engineer",
            "difficulty": "Medium",
            "round_title": "Round 1: Aptitude"
        }
        start_res = self.client.post("/api/interview/sessions", json=payload, headers=self.headers)
        session_id = start_res.json()["id"]

        comp_res = self.client.post(f"/api/interview/sessions/{session_id}/complete", headers=self.headers)
        self.assertEqual(comp_res.status_code, 200, comp_res.text)
        feedback = comp_res.json()

        self.assertTrue(feedback["completed"])
        self.assertIn("summary", feedback)
        self.assertIn("strengths", feedback)
        self.assertIn("weaknesses", feedback)
        self.assertIn("recommendations", feedback)
        self.assertIn("overall_score", feedback)

    def test_onboarding_difficulty_selection(self) -> None:
        """Requirement 2: Verify difficulty selection in onboarding flow and persistence in profile."""
        onboarding_payload = {
            "user_type": "Graduate",
            "career_goal": "Placement",
            "company_type": "Product-based",
            "dream_company": "Google",
            "target_role": "Full Stack Developer",
            "current_level": "Intermediate",
            "interview_difficulty": "Hard",
            "skills": ["Python", "React", "Aptitude"]
        }
        ob_res = self.client.post("/api/onboarding/", json=onboarding_payload, headers=self.headers)
        self.assertEqual(ob_res.status_code, 200, ob_res.text)

        profile_res = self.client.get("/api/onboarding/me", headers=self.headers)
        self.assertEqual(profile_res.status_code, 200, profile_res.text)
        profile_data = profile_res.json()
        self.assertEqual(profile_data["target_company"], "Google")
        self.assertEqual(profile_data["target_role"], "Full Stack Developer")
        self.assertEqual(profile_data["interview_difficulty"], "Hard")

    def test_round1_aptitude_purity_and_difficulty_validation(self) -> None:
        """
        Requirement 1, 3, 4:
        - Round 1 contains strictly Aptitude & Logical reasoning questions.
        - Exactly 10 questions.
        - 4 MCQ options.
        - Exactly one correct answer matching options.
        - No duplicate questions.
        - ZERO programming/coding questions in Round 1.
        - Selected difficulty reaches generator and matches session.
        - Company-specific question pools used.
        """
        companies = ["TCS", "Infosys", "Zoho", "Google", "Amazon", "Microsoft", "Startup"]
        difficulties = ["Easy", "Medium", "Hard"]

        forbidden_coding_keywords = [
            "python", "java", "c++", "code", "coding", "function", "array", "string",
            "loop", "algorithm", "data structure", "class ", "variable", "pointer",
            "linked list", "tree", "graph", "stack", "queue", "hashmap", "binary search",
            "time complexity", "space complexity", "o(n)"
        ]

        sample_questions_by_difficulty = {}

        for diff in difficulties:
            sample_questions_by_difficulty[diff] = []
            for company in companies:
                payload = {
                    "company_name": company,
                    "role": "Software Engineer",
                    "difficulty": diff,
                    "round_title": "Round 1: Aptitude & Logic"
                }
                res = self.client.post("/api/interview/sessions", json=payload, headers=self.headers)
                self.assertEqual(res.status_code, 200, res.text)
                session = res.json()

                # Verify selected difficulty reaches session
                self.assertEqual(session["difficulty"], diff)
                self.assertEqual(session["role"], "Software Engineer")

                questions = session["questions"]
                self.assertEqual(len(questions), 10, f"Round 1 for {company} {diff} did not return 10 questions!")

                prompts = [q["prompt"] for q in questions]
                # Assert no duplicate questions
                self.assertEqual(len(prompts), len(set(prompts)), f"Duplicate questions in Round 1 for {company} {diff}!")

                for q in questions:
                    # Assert 4 MCQ options
                    options = q.get("options")
                    self.assertIsNotNone(options, f"Missing options in MCQ for prompt: {q['prompt']}")
                    self.assertEqual(len(options), 4, f"Option count != 4 for prompt: {q['prompt']}")

                    # Assert correct answer is present in options
                    correct_answer = q.get("correct_answer")
                    self.assertIsNotNone(correct_answer, f"Missing correct_answer for prompt: {q['prompt']}")
                    self.assertIn(correct_answer, options, f"Correct answer '{correct_answer}' not in options {options}")

                    # Assert ZERO programming/coding questions in Round 1
                    prompt_lower = q["prompt"].lower()
                    for keyword in forbidden_coding_keywords:
                        pattern = rf"\b{re.escape(keyword.strip())}\b" if " " not in keyword else re.escape(keyword)
                        self.assertIsNone(
                            re.search(pattern, prompt_lower),
                            f"Coding keyword '{keyword}' found in Round 1 Aptitude prompt: {q['prompt']}"
                        )

                # Store sample question for report
                sample_questions_by_difficulty[diff].append(questions[0]["prompt"])

        # Compare Easy vs Medium vs Hard sets to confirm difficulty variation
        easy_q = set(sample_questions_by_difficulty["Easy"])
        hard_q = set(sample_questions_by_difficulty["Hard"])
        self.assertNotEqual(easy_q, hard_q, "Easy and Hard difficulty produced identical Round 1 questions!")


if __name__ == "__main__":
    unittest.main()

