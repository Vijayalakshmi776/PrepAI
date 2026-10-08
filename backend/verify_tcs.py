import uuid
import httpx
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def main():
    client = httpx.Client(base_url=BASE_URL, timeout=60.0)
    
    uid = str(uuid.uuid4())[:8]
    email = f"tcs_candidate_{uid}@example.com"
    password = "SecurePassword123!"
    
    print("\n1. Register & Login")
    client.post("/auth/register", json={"email": email, "full_name": f"TCS {uid}", "password": password})
    token = client.post("/auth/token", json={"email": email, "password": password}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n2. Onboarding")
    client.post("/onboarding/", json={
        "user_type": "College Student",
        "career_goal": "Product Company Placement",
        "company_type": "Service-based",
        "dream_company": "TCS",
        "target_role": "Frontend Developer",
        "current_level": "Beginner",
        "skills": ["HTML", "CSS", "React"]
    }, headers=headers)
    
    print("\n3. Start TCS Mock Interview")
    session_payload = {
        "company_name": "TCS",
        "role": "Frontend Developer",
        "difficulty": "Easy"
    }
    session_resp = client.post("/interview/sessions", json=session_payload, headers=headers)
    session_data = session_resp.json()
    session_id = session_data["id"]
    questions = session_data["questions"]
    
    print(f"\n[SESSION CREATED] {session_data['title']} (ID: {session_id})")
    print(f"Round 1: {session_data['current_round']['title']}")
    print(f"Questions Count: {len(questions)}")
    
    print("\n--- FIRST 5 APTITUDE QUESTIONS ---")
    for i in range(min(5, len(questions))):
        q = questions[i]
        print(f"\nQ{i+1}:")
        print(f"Prompt: {q['prompt']}")
        print(f"Options: {q['options']}")
        
    print("\n4. Submit Answers for all 10 Aptitude questions")
    score_sum = 0
    # Guess the first option for all questions just to move forward
    for i, q in enumerate(questions):
        opt = q['options'][0] if q['options'] else "dummy"
        ans_resp = client.post(f"/interview/questions/{q['id']}/answer", json={"response": opt}, headers=headers)
        if ans_resp.status_code == 200:
            score_sum += ans_resp.json()["score"]
    
    print(f"Total Aptitude Score (random guessing): {score_sum} / {len(questions)*100}")
    
    print("\n5. Advance to Next Round")
    next_round_resp = client.post(f"/interview/sessions/{session_id}/next-round", headers=headers)
    next_round_data = next_round_resp.json()
    print(f"Round 2: {next_round_data['current_round']['title']}")
    
    # Complete the interview
    print("\n6. Complete Interview")
    complete_resp = client.post(f"/interview/sessions/{session_id}/complete", headers=headers)
    print("Interview Completed!")
    
    print("\n7. Fetch Dashboard Readiness")
    profile = client.get("/auth/me", headers=headers).json()
    print(f"Overall Readiness Score: {profile.get('readiness_score', 'N/A')}")
    
if __name__ == "__main__":
    main()
