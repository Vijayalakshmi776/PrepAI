import os
import sys
import uuid
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from app.main import app

def verify_mock_interview_flow():
    print("====================================================================")
    print("VERIFYING MOCK INTERVIEW FIXES (BUG 1 & BUG 2)")
    print("====================================================================")
    client = TestClient(app)

    # 1. Register candidate
    uid = str(uuid.uuid4())[:8]
    email = f"mock_candidate_{uid}@example.com"
    password = "Password123!"

    print(f"\n[Step 1] Registering user: {email}...")
    r = client.post("/api/auth/register", json={"email": email, "full_name": f"Candidate {uid}", "password": password})
    assert r.status_code == 201, f"Registration failed: {r.text}"

    # 2. Login
    r = client.post("/api/auth/token", json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("  [PASS] Logged in successfully.")

    # 3. Fetch Company Catalog
    print("\n[Step 2] Fetching Company Catalog...")
    r = client.get("/api/interview/companies", headers=headers)
    assert r.status_code == 200
    companies = r.json()
    company_names = [c["name"] for c in companies]
    print(f"  [PASS] Available companies: {company_names}")
    assert "Zoho" in company_names, "Zoho missing from company catalog"

    # 4. Start Mock Interview with selected Company = Zoho, Difficulty = Hard
    selected_company = "Zoho"
    selected_role = "Full Stack Developer"
    selected_difficulty = "Hard"

    print(f"\n[Step 3] Starting Mock Interview for {selected_company} ({selected_difficulty})...")
    payload = {
        "company_name": selected_company,
        "role": selected_role,
        "difficulty": selected_difficulty,
        "round_title": "Round 1: Aptitude & Logic"
    }
    r = client.post("/api/interview/sessions", json=payload, headers=headers)
    assert r.status_code == 200, f"Start session failed: {r.text}"
    session_data = r.json()
    session_id = session_data["id"]
    
    assert session_data["company_name"] == selected_company, f"Expected {selected_company}, got {session_data['company_name']}"
    assert session_data["difficulty"] == selected_difficulty, f"Expected {selected_difficulty}, got {session_data['difficulty']}"
    assert len(session_data["questions"]) > 0, "No questions generated"
    print(f"  [PASS] Session created cleanly (ID: {session_id}) with {len(session_data['questions'])} questions.")

    # 5. Answer all questions including final question
    questions = session_data["questions"]
    print(f"\n[Step 4] Answering {len(questions)} questions...")
    for idx, q in enumerate(questions):
        ans_text = q.get("options", ["Sample answer"])[0] if q.get("options") else "Detailed technical answer explanation."
        resp = client.post(f"/api/interview/questions/{q['id']}/answer", json={"response": ans_text}, headers=headers)
        assert resp.status_code == 200, f"Answer q{idx+1} failed: {resp.text}"
        ans_res = resp.json()
        assert "score" in ans_res
    print("  [PASS] All questions submitted and evaluated.")

    # 6. Finish & Review Summary
    print("\n[Step 5] Completing Interview Session (Finish & Review Summary)...")
    comp_resp = client.post(f"/api/interview/sessions/{session_id}/complete", headers=headers)
    assert comp_resp.status_code == 200, f"Complete session failed: {comp_resp.text}"
    summary = comp_resp.json()
    assert summary["completed"] is True
    assert "summary" in summary
    assert "overall_score" in summary
    print(f"  [PASS] Session completed. Overall Score: {summary['overall_score']}%. Summary: {summary['summary'][:60]}...")

    # 7. Refresh Page Simulation (Fetch session by ID)
    print("\n[Step 6] Simulating Page Refresh on Summary View (Get Session Details)...")
    get_resp = client.get(f"/api/interview/sessions/{session_id}", headers=headers)
    assert get_resp.status_code == 200
    refreshed_session = get_resp.json()
    assert refreshed_session["completed"] is True
    assert refreshed_session["feedback"] is not None
    assert len(refreshed_session["questions"]) == len(questions)
    print("  [PASS] Refreshed session retained completed state, feedback summary, and question logs.")

    # 8. Check Past Sessions History
    print("\n[Step 7] Checking Past Sessions History...")
    list_resp = client.get("/api/interview/sessions", headers=headers)
    assert list_resp.status_code == 200
    past_sessions = list_resp.json()
    matching = [s for s in past_sessions if s["id"] == session_id]
    assert len(matching) == 1, "Completed session not found in history"
    assert matching[0]["completed"] is True
    print("  [PASS] Completed session appears in user history.")

    print("\n====================================================================")
    print("ALL MOCK INTERVIEW FIX VERIFICATIONS PASSED WITH 100% SUCCESS!")
    print("====================================================================\n")

if __name__ == "__main__":
    verify_mock_interview_flow()
