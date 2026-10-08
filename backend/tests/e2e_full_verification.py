import io
import json
import os
import sys
import unittest
import uuid
import httpx

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

BASE_URL = "http://127.0.0.1:8000/api"

SAMPLE_PDF_BYTES = b"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length 320 >>
stream
BT
/F1 12 Tf
72 712 Td
(Jordan Smith) Tj
0 -18 Td
(jordan.smith@example.com | 555-987-6543 | github.com/jordansmith | linkedin.com/in/jordansmith) Tj
0 -18 Td
(Software Engineer specializing in Python, React, PostgreSQL, Docker, and REST APIs.) Tj
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
0000000607 00000 n 
trailer << /Size 6 /Root 1 0 R >>
startxref
678
%%EOF"""


from fastapi.testclient import TestClient
from app.main import app

def run_live_e2e_verification():
    print("====================================================================")
    print("STARTING FULL LIVE END-TO-END PRODUCT VERIFICATION (PREPAI)")
    print("Target: In-Memory FastAPI App TestClient")
    print("====================================================================")

    client = TestClient(app)

    # 1. Register
    uid = str(uuid.uuid4())[:8]
    email = f"candidate_live_{uid}@example.com"
    full_name = f"Candidate Live {uid}"
    password = "SecurePassword123!"

    print("\n[Step 1] Testing User Registration...")
    reg_resp = client.post("/api/auth/register", json={
        "email": email,
        "full_name": full_name,
        "password": password
    })
    assert reg_resp.status_code == 201, f"Registration failed: {reg_resp.text}"
    reg_data = reg_resp.json()
    assert reg_data["email"] == email
    print(f"  [PASS] Registered: {email} (ID: {reg_data['id']})")

    # 2. Login
    print("\n[Step 2] Testing User Login & JWT Generation...")
    login_resp = client.post("/api/auth/token", json={
        "email": email,
        "password": password
    })
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token_data = login_resp.json()
    assert "access_token" in token_data
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("  [PASS] Login successful. JWT Token received and verified.")

    # 3. Protected /auth/me
    print("\n[Step 3] Testing Protected Route /api/auth/me...")
    me_resp = client.get("/api/auth/me", headers=headers)
    assert me_resp.status_code == 200, f"Auth me failed: {me_resp.text}"
    assert me_resp.json()["email"] == email
    print(f"  [PASS] User profile verified: {me_resp.json()['full_name']}")

    # 4. Onboarding
    print("\n[Step 4] Testing Onboarding Flow...")
    onboarding_payload = {
        "user_type": "College Student",
        "career_goal": "Product Company Placement",
        "company_type": "Product-based",
        "dream_company": "Google",
        "target_role": "Software Engineer",
        "current_level": "Intermediate",
        "skills": ["Python", "Data Structures", "Algorithms", "PostgreSQL"]
    }
    onboard_resp = client.post("/api/onboarding/", json=onboarding_payload, headers=headers)
    assert onboard_resp.status_code == 200, f"Onboarding failed: {onboard_resp.text}"
    assert onboard_resp.json()["status"] == "ok"
    print("  [PASS] Onboarding saved successfully.")

    profile_resp = client.get("/api/onboarding/me", headers=headers)
    assert profile_resp.status_code == 200
    profile_data = profile_resp.json()
    assert profile_data["target_company"] == "Google"
    assert profile_data["target_role"] == "Software Engineer"
    print(f"  [PASS] Onboarding profile verified: Target Company = {profile_data['target_company']}, Role = {profile_data['target_role']}")

    # 5. Mock Interview Flow
    print("\n[Step 5] Testing Mock Interview Flow...")
    comp_resp = client.get("/api/interview/companies")
    assert comp_resp.status_code == 200
    companies = comp_resp.json()
    assert len(companies) > 0
    print(f"  [PASS] Fetched {len(companies)} interview company catalogs.")

    # Start session
    session_payload = {
        "company_name": "Google",
        "role": "Software Engineer",
        "difficulty": "Medium"
    }
    session_resp = client.post("/api/interview/sessions", json=session_payload, headers=headers)
    assert session_resp.status_code == 200, f"Interview start failed: {session_resp.text}"
    session_data = session_resp.json()
    session_id = session_data["id"]
    questions = session_data["questions"]
    assert len(questions) > 0
    print(f"  [PASS] Started Mock Interview session: {session_id} with {len(questions)} questions.")

    # Answer first question
    q_id = questions[0]["id"]
    ans_resp = client.post(f"/api/interview/questions/{q_id}/answer", json={
        "response": "To traverse a large graph and find strongly connected components, we can use Tarjan's algorithm with DFS discovery and low-link values in O(V+E) time complexity."
    }, headers=headers)
    assert ans_resp.status_code == 200, f"Answer submit failed: {ans_resp.text}"
    ans_data = ans_resp.json()
    print(f"  [PASS] Answer scored by AI: {ans_data['score']}/100 - Feedback: {ans_data['feedback'][:70]}...")

    # Complete session
    comp_session_resp = client.post(f"/api/interview/sessions/{session_id}/complete", headers=headers)
    assert comp_session_resp.status_code == 200
    feedback_data = comp_session_resp.json()
    print(f"  [PASS] Interview completed. Summary: {feedback_data['summary'][:70]}...")

    # 6. Roadmap Flow
    print("\n[Step 6] Testing Personalized Roadmap Flow...")
    roadmap_resp = client.get("/api/roadmap/me", headers=headers)
    assert roadmap_resp.status_code == 200, f"Roadmap fetch failed: {roadmap_resp.text}"
    roadmap_data = roadmap_resp.json()
    assert "roadmap_id" in roadmap_data
    assert roadmap_data["target_company"] == "Google"
    assert len(roadmap_data["tasks"]) > 0
    assert len(roadmap_data["skill_gaps"]) > 0
    assert len(roadmap_data["company_recommendations"]) > 0
    print(f"  [PASS] Roadmap loaded: '{roadmap_data['title']}' ({len(roadmap_data['tasks'])} learning tasks, {len(roadmap_data['skill_gaps'])} skill gaps)")

    # Toggle task
    first_task = roadmap_data["tasks"][0]
    toggle_resp = client.patch(f"/api/roadmap/tasks/{first_task['id']}/toggle", headers=headers)
    assert toggle_resp.status_code == 200, f"Toggle failed: {toggle_resp.text}"
    toggle_data = toggle_resp.json()
    assert toggle_data["completed"] is True
    assert toggle_data["progress"]["completed_count"] == 1
    assert toggle_data["progress"]["xp_points"] == 50
    print(f"  [PASS] Task '{first_task['title']}' completed. Progress: {toggle_data['progress']['completion_percentage']}% (+50 XP).")

    # 7. Resume Analysis Flow
    print("\n[Step 7] Testing Resume Analysis Flow & Role Suitability Grounding...")
    files = {"file": ("jordan_smith_resume.pdf", io.BytesIO(SAMPLE_PDF_BYTES), "application/pdf")}
    resume_resp = client.post("/api/resume/analyze", files=files, data={"target_role": "Software Engineer"}, headers=headers)
    assert resume_resp.status_code == 201, f"Resume analyze failed: {resume_resp.text}"
    resume_data = resume_resp.json()
    resume_id = resume_data["resume_id"]
    assert resume_data["readiness_score"] > 0
    assert resume_data["role_suitability_score"] > 0
    assert resume_data["ats_score"] > 0
    assert len(resume_data["detected_skills"]) > 0
    assert len(resume_data["strengths"]) > 0
    assert len(resume_data["recommendations"]) > 0
    assert "role_suitability_explanation" in resume_data
    
    # Verify recommended roles threshold and anti-hallucination
    rec_roles = [r["role"].lower() for r in resume_data["job_role_recommendations"]]
    for r in resume_data["job_role_recommendations"]:
        assert r["match_percentage"] >= 55.0, f"Match percentage below threshold: {r}"
    assert "data scientist" not in rec_roles, "Hallucinated Data Scientist for backend software engineer resume!"
    assert "cybersecurity engineer" not in rec_roles, "Hallucinated Cybersecurity Engineer!"
    
    print(f"  [PASS] PDF parsed & analyzed. Overall Score: {resume_data['readiness_score']}%, Role Suitability: {resume_data['role_suitability_score']}%, ATS Score: {resume_data['ats_score']}%.")
    print(f"    Detected Skills: {', '.join(resume_data['detected_skills'])}")
    print(f"    Grounded Recommended Roles: {[r['role'] + ' (' + str(r['match_percentage']) + '%)' for r in resume_data['job_role_recommendations']]}")

    # Test Role Switching (Switch target role to AI/ML Engineer for same user)
    files_switch = {"file": ("jordan_smith_resume.pdf", io.BytesIO(SAMPLE_PDF_BYTES), "application/pdf")}
    switch_resp = client.post("/api/resume/analyze", files=files_switch, data={"target_role": "AI/ML Engineer"}, headers=headers)
    assert switch_resp.status_code == 201
    switch_data = switch_resp.json()
    assert switch_data["target_role"] == "AI/ML Engineer"
    assert switch_data["role_suitability_score"] < resume_data["role_suitability_score"], "Role suitability score did not adjust for missing ML skills!"
    print(f"  [PASS] Role switching verified: AI/ML Engineer suitability dropped to {switch_data['role_suitability_score']}% as expected.")

    # Fetch latest & history
    latest_resp = client.get("/api/resume/latest", headers=headers)
    assert latest_resp.status_code == 200
    assert latest_resp.json()["resume_id"] == switch_data["resume_id"]
    print("  [PASS] Latest resume analysis verified.")

    hist_resp = client.get("/api/resume/history", headers=headers)
    assert hist_resp.status_code == 200
    history = hist_resp.json()
    assert len(history) >= 2
    print(f"  [PASS] Resume history verified ({len(history)} analyses in history).")

    # 8. Cross-User Authorization Verification
    print("\n[Step 8] Testing Cross-User Security & Authorization...")
    uid2 = str(uuid.uuid4())[:8]
    client.post("/api/auth/register", json={
        "email": f"attacker_{uid2}@example.com",
        "full_name": f"Attacker {uid2}",
        "password": "AttackerPass123!"
    })
    login2 = client.post("/api/auth/token", json={
        "email": f"attacker_{uid2}@example.com",
        "password": "AttackerPass123!"
    })
    headers2 = {"Authorization": f"Bearer {login2.json()['access_token']}"}

    # User 2 attempting to modify User 1's roadmap task -> 403 Forbidden
    task_attack = client.patch(f"/api/roadmap/tasks/{first_task['id']}/toggle", headers=headers2)
    assert task_attack.status_code == 403, f"Expected 403, got {task_attack.status_code}"
    print("  [PASS] Cross-user task tampering blocked with 403 Forbidden.")

    # User 2 attempting to view User 1's resume analysis -> 403 Forbidden
    resume_attack = client.get(f"/api/resume/{resume_id}", headers=headers2)
    assert resume_attack.status_code == 403, f"Expected 403, got {resume_attack.status_code}"
    print("  [PASS] Cross-user resume access blocked with 403 Forbidden.")

    print("\n====================================================================")
    print("ALL LIVE END-TO-END PRODUCT FLOWS PASSED WITH 100% SUCCESS!")
    print("====================================================================")


if __name__ == "__main__":
    run_live_e2e_verification()
