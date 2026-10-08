import io
import unittest
import uuid
from fastapi.testclient import TestClient
from app.main import app

SAMPLE_PDF_BYTES = b"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length 300 >>
stream
BT
/F1 12 Tf
72 712 Td
(Jordan Smith) Tj
0 -18 Td
(jordan.smith@example.com | 555-987-6543 | github.com/jordansmith) Tj
0 -18 Td
(Software Engineer with expertise in Python, React, PostgreSQL, Docker, and REST APIs.) Tj
0 -18 Td
(Architected distributed backend pipelines, improving query latency by 40% across 250k daily active users.) Tj
0 -18 Td
(Implemented CI/CD pipelines in Git and managed automated unit testing suites.) Tj
ET
endstream
endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000060 00000 n 
0000000117 00000 n 
0000000234 00000 n 
0000000587 00000 n 
trailer << /Size 6 /Root 1 0 R >>
startxref
658
%%EOF"""


class ResumeAnalysisIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        uid = str(uuid.uuid4())[:8]
        self.email = f"resume_user_{uid}@example.com"
        self.password = "securepass123"
        self.client.post("/api/auth/register", json={
            "email": self.email,
            "full_name": f"Resume Student {uid}",
            "password": self.password
        })
        login_res = self.client.post("/api/auth/token", json={
            "email": self.email,
            "password": self.password
        })
        self.token = login_res.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

        # Complete onboarding
        self.client.post("/api/onboarding/", json={
            "user_type": "College Student",
            "career_goal": "Product Company Placement",
            "company_type": "Product-based",
            "dream_company": "Google",
            "target_role": "Software Engineer",
            "current_level": "Intermediate",
            "skills": ["Python", "Data Structures", "PostgreSQL"]
        }, headers=self.headers)

    def test_resume_analysis_full_lifecycle(self) -> None:
        # 1. Unauthenticated upload fails with 401
        files = {"file": ("resume.pdf", io.BytesIO(SAMPLE_PDF_BYTES), "application/pdf")}
        unauth_res = self.client.post("/api/resume/analyze", files=files)
        self.assertEqual(unauth_res.status_code, 401)

        # 2. Invalid file format rejection (e.g. txt file)
        invalid_file = {"file": ("resume.txt", io.BytesIO(b"Just plain text resume"), "text/plain")}
        inv_res = self.client.post("/api/resume/analyze", files=invalid_file, headers=self.headers)
        self.assertEqual(inv_res.status_code, 400)

        # 3. Empty PDF rejection
        empty_file = {"file": ("empty.pdf", io.BytesIO(b""), "application/pdf")}
        empty_res = self.client.post("/api/resume/analyze", files=empty_file, headers=self.headers)
        self.assertEqual(empty_res.status_code, 400)

        # 4. Valid PDF upload and analysis
        valid_file = {"file": ("jordan_smith_resume.pdf", io.BytesIO(SAMPLE_PDF_BYTES), "application/pdf")}
        upload_res = self.client.post("/api/resume/analyze", files=valid_file, headers=self.headers)
        self.assertEqual(upload_res.status_code, 201, upload_res.text)
        data = upload_res.json()

        self.assertIn("id", data)
        self.assertIn("resume_id", data)
        self.assertEqual(data["title"], "jordan_smith_resume.pdf")
        self.assertGreater(data["readiness_score"], 0)
        self.assertGreater(data["ats_score"], 0)
        self.assertGreater(len(data["detected_skills"]), 0)
        self.assertGreater(len(data["strengths"]), 0)
        self.assertGreater(len(data["recommendations"]), 0)
        self.assertEqual(data["target_role"], "Software Engineer")
        self.assertEqual(data["target_company"], "Google")

        resume_id = data["resume_id"]
        analysis_id = data["id"]

        # 5. Fetch latest analysis (GET /api/resume/latest)
        latest_res = self.client.get("/api/resume/latest", headers=self.headers)
        self.assertEqual(latest_res.status_code, 200, latest_res.text)
        latest_data = latest_res.json()
        self.assertEqual(latest_data["resume_id"], resume_id)
        self.assertEqual(latest_data["id"], analysis_id)

        # 6. Fetch specific resume by ID (GET /api/resume/{resume_id})
        by_id_res = self.client.get(f"/api/resume/{resume_id}", headers=self.headers)
        self.assertEqual(by_id_res.status_code, 200, by_id_res.text)
        self.assertEqual(by_id_res.json()["resume_id"], resume_id)

        # 7. Fetch history list (GET /api/resume/history)
        hist_res = self.client.get("/api/resume/history", headers=self.headers)
        self.assertEqual(hist_res.status_code, 200, hist_res.text)
        history = hist_res.json()
        self.assertGreaterEqual(len(history), 1)
        self.assertEqual(history[0]["resume_id"], resume_id)

        # 8. User 2 Authorization / Ownership Protection
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

        # User 2 cannot access User 1's resume
        cross_res = self.client.get(f"/api/resume/{resume_id}", headers=headers2)
        self.assertEqual(cross_res.status_code, 403)

        # User 2 cannot delete User 1's resume
        cross_del = self.client.delete(f"/api/resume/{resume_id}", headers=headers2)
        self.assertEqual(cross_del.status_code, 403)

        # 9. User 1 deletes their resume
        del_res = self.client.delete(f"/api/resume/{resume_id}", headers=self.headers)
        self.assertEqual(del_res.status_code, 200)

        # 10. After deletion, GET /api/resume/{resume_id} returns 404
        post_del = self.client.get(f"/api/resume/{resume_id}", headers=self.headers)
        self.assertEqual(post_del.status_code, 404)

    def test_target_role_switching_and_anti_hallucination(self) -> None:
        # Sample Frontend PDF Resume
        frontend_pdf_bytes = b"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length 320 >>
stream
BT
/F1 12 Tf
72 712 Td
(Alex Rivera - Web Developer) Tj
0 -18 Td
(alex.rivera@example.com | 555-123-4567 | github.com/arivera) Tj
0 -18 Td
(Skills: HTML, CSS, JavaScript, React, Python, MySQL, Git.) Tj
0 -18 Td
(Projects: Responsive Web Dashboard built with React, HTML5, CSS3, JavaScript and MySQL backend.) Tj
ET
endstream
endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000060 00000 n 
0000000117 00000 n 
0000000234 00000 n 
0000000607 00000 n 
trailer << /Size 6 /Root 1 0 R >>
startxref
678
%%EOF"""

        # 1. Analyze for Frontend Developer
        files1 = {"file": ("alex_frontend_resume.pdf", io.BytesIO(frontend_pdf_bytes), "application/pdf")}
        res1 = self.client.post("/api/resume/analyze", files=files1, data={"target_role": "Frontend Developer"}, headers=self.headers)
        self.assertEqual(res1.status_code, 201, res1.text)
        data1 = res1.json()

        self.assertEqual(data1["target_role"], "Frontend Developer")
        self.assertGreater(data1["role_suitability_score"], 50.0)
        self.assertIn("HTML", [s.upper() for s in data1["matching_skills"]])
        self.assertIn("React", data1["matching_skills"])

        # Check recommended roles for anti-hallucination
        rec_roles1 = [r["role"].lower() for r in data1["job_role_recommendations"]]
        self.assertTrue(any(role in ["frontend developer", "react developer", "ui developer", "full stack developer"] for role in rec_roles1))
        # Ensure Data Scientist / DevOps / Cybersecurity are NOT in recommendations
        self.assertNotIn("data scientist", rec_roles1)
        self.assertNotIn("cloud / devops engineer", rec_roles1)
        self.assertNotIn("cybersecurity engineer", rec_roles1)

        # 2. Analyze SAME resume for AI/ML Engineer
        files2 = {"file": ("alex_frontend_resume.pdf", io.BytesIO(frontend_pdf_bytes), "application/pdf")}
        res2 = self.client.post("/api/resume/analyze", files=files2, data={"target_role": "AI/ML Engineer"}, headers=self.headers)
        self.assertEqual(res2.status_code, 201, res2.text)
        data2 = res2.json()

        self.assertEqual(data2["target_role"], "AI/ML Engineer")
        # Suitability score for AI/ML Engineer must be lower because resume lacks ML evidence (only Python)
        self.assertLess(data2["role_suitability_score"], data1["role_suitability_score"])
        self.assertIn("Machine Learning", data2["missing_skills"])


if __name__ == "__main__":
    unittest.main()

