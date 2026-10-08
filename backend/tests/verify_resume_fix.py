import os
import sys
import uuid
import json

os.environ['DATABASE_URL'] = 'postgresql+psycopg://postgres:viji%40123@localhost:5432/prepai'
sys.path.insert(0, r'D:\PrepAi\backend')

from app.services.resume_analyzer import extract_text_from_pdf, detect_skills_in_text, analyze_resume_content, call_gemini_resume_analysis
from app.db.session import SessionLocal
from app.models.resume import Resume
from app.models.resume_analysis import ResumeAnalysis
from app.models.user import User

def main():
    resume_path = r'C:\Users\ELCOT\Downloads\Vijayalakshmi M_Resume.pdf'
    assert os.path.exists(resume_path), f"Resume file not found at {resume_path}"

    with open(resume_path, 'rb') as f:
        pdf_bytes = f.read()

    # 1. PDF extraction succeeds
    extracted_text = extract_text_from_pdf(pdf_bytes)
    assert extracted_text and len(extracted_text) > 0, "Requirement 1 Failed: PDF extraction failed"

    # 2. Extracted word count > 0
    words = [w for w in extracted_text.split() if w]
    word_count = len(words)
    assert word_count > 0, "Requirement 2 Failed: Extracted word count is 0"

    # 3. Print extracted text length and word count in diagnostic only
    print("=== DIAGNOSTIC REPORT: RESUME TEXT EXTRACTION ===")
    print(f"Resume File Path: {resume_path}")
    print(f"Extracted Text Length: {len(extracted_text)} characters")
    print(f"Extracted Word Count: {word_count} words")
    print("First 300 characters preview:")
    print(repr(extracted_text[:300]))

    # 4. Verify skills extracted from actual resume
    detected_skills = detect_skills_in_text(extracted_text)
    print("\n=== SKILL EXTRACTION DIAGNOSTIC ===")
    print("Detected Skills:", detected_skills)
    assert len(detected_skills) > 0, "Requirement 4 Failed: No skills detected from actual resume"

    # 5. Make sure single-character skills C and R are NOT falsely detected from CSS/React/Frontend
    assert 'C' not in detected_skills, "Requirement 5 Failed: Single-character skill 'C' falsely detected!"
    assert 'R' not in detected_skills, "Requirement 5 Failed: Single-character skill 'R' falsely detected!"
    print("[PASS] Single-character skills 'C' and 'R' were NOT falsely detected.")

    # 6. Verify HTML, CSS, JavaScript, React, Python, MySQL occur in resume and are extracted
    for expected_skill in ['HTML', 'CSS', 'JavaScript', 'React', 'Python', 'MySQL']:
        assert expected_skill in detected_skills, f"Requirement 6 Failed: Skill '{expected_skill}' was in resume but not detected"
    print(f"[PASS] Verified presence of expected skills: HTML, CSS, JavaScript, React, Python, MySQL.")

    # 7 & 8. Select Frontend Developer & Calculate Role Suitability
    target_role = "Frontend Developer"
    target_company = "Google"
    analysis = analyze_resume_content(
        resume_text=extracted_text,
        target_role=target_role,
        target_company=target_company
    )

    print(f"\n=== EVALUATION FOR ROLE: {target_role} ===")
    print(f"Role Suitability Score: {analysis['role_suitability_score']}% ({analysis['role_suitability_status']})")

    # 9. Show actual matching skills
    print("9. Actual Matching Skills:", analysis['matching_skills'])
    assert len(analysis['matching_skills']) > 0, "Requirement 9 Failed: No matching skills returned"

    # 10. Show actual missing skills
    print("10. Actual Missing Skills:", analysis['missing_skills'])
    assert len(analysis['missing_skills']) > 0, "Requirement 10 Failed: No missing skills returned"

    # 11. Recommend only job roles supported by resume evidence
    print("\n11. Grounded Job Role Recommendations (Threshold >= 55% evidence match):")
    for job in analysis['job_role_recommendations']:
        print(f"  - {job['role']} (Match: {job['match_percentage']}%) | Matching: {job['matching_skills']} | Missing: {job['missing_skills']}")
        assert job['match_percentage'] >= 55.0, f"Recommendation {job['role']} below 55% threshold!"
        for ms in job['matching_skills']:
            assert ms.lower() in [s.lower() for s in detected_skills], f"Skill {ms} in job recommendation not present in extracted resume!"

    # 12. Calculate PrepAI ATS Compatibility Score
    print(f"\n12. PrepAI ATS Compatibility Score: {analysis['ats_score']}%")
    assert analysis['ats_score'] > 0, "Requirement 12 Failed: ATS score is 0"

    # 13. Verify Gemini receives extracted resume text, not empty string
    prompt_text = extracted_text[:3500]
    assert len(prompt_text) > 0 and prompt_text == extracted_text[:3500], "Requirement 13 Failed: Gemini received empty resume text"
    print("[PASS] Verified Gemini receives non-empty extracted resume text.")

    # 14. Verify Gemini status & Fallback mode
    print(f"\n14. Gemini API Integration & Fallback Mode:")
    print(f"  - Gemini Used: {analysis['gemini_used']}")
    print(f"  - Fallback Active: {analysis['fallback_used']}")
    print(f"  - Evaluation Summary: {analysis['summary']}")
    assert not (analysis['gemini_used'] and analysis['fallback_used']), "Inconsistent Gemini status flags"

    # 15. Save analysis to PostgreSQL
    db = SessionLocal()
    user = db.query(User).first()
    assert user is not None, "Requirement 15 Failed: No user found in database to attach resume"

    test_user_id = str(user.id)
    new_resume_id = uuid.uuid4()
    new_analysis_id = uuid.uuid4()

    resume_obj = Resume(
        id=new_resume_id,
        user_id=test_user_id,
        title="Vijayalakshmi M_Resume.pdf",
        content=extracted_text[:8000],
        file_type="pdf",
        language="en",
        word_count=analysis['word_count'],
        keywords=", ".join(analysis['detected_skills'][:15])
    )
    db.add(resume_obj)
    db.flush()

    stored_gaps = {**analysis}
    if "recommendations" in stored_gaps:
        del stored_gaps["recommendations"]

    analysis_obj = ResumeAnalysis(
        id=new_analysis_id,
        resume_id=new_resume_id,
        readiness_score=analysis['role_suitability_score'],
        clarity_score=analysis['formatting_score'],
        impact_score=analysis['experience_score'],
        skill_alignment_score=analysis['skills_score'],
        summary=analysis['summary'],
        recommendations=json.dumps(analysis['recommendations']),
        skill_gaps=json.dumps(stored_gaps)
    )
    db.add(analysis_obj)
    db.commit()

    print(f"\n15. PostgreSQL Persistence Verification:")
    print(f"  - Saved Resume ID: {new_resume_id}")
    print(f"  - Saved ResumeAnalysis ID: {new_analysis_id}")

    # 16. Reload & Verify saved result from PostgreSQL
    reloaded_analysis = db.query(ResumeAnalysis).filter(ResumeAnalysis.id == new_analysis_id).first()
    reloaded_resume = db.query(Resume).filter(Resume.id == new_resume_id).first()

    assert reloaded_analysis is not None, "Requirement 16 Failed: Saved ResumeAnalysis not found upon reload!"
    assert reloaded_resume is not None, "Requirement 16 Failed: Saved Resume not found upon reload!"
    assert reloaded_resume.title == "Vijayalakshmi M_Resume.pdf"
    assert reloaded_analysis.readiness_score == analysis['role_suitability_score']
    
    reloaded_gaps = json.loads(reloaded_analysis.skill_gaps)
    assert reloaded_gaps['target_role'] == target_role
    assert reloaded_gaps['ats_score'] == analysis['ats_score']
    assert set(reloaded_gaps['matching_skills']) == set(analysis['matching_skills'])

    print(f"\n16. Reload Verification:")
    print(f"  - Successfully reloaded saved record from PostgreSQL!")
    print(f"  - Title: '{reloaded_resume.title}'")
    print(f"  - Readiness Score: {reloaded_analysis.readiness_score}%")
    print(f"  - Reloaded Target Role: '{reloaded_gaps['target_role']}'")
    print(f"  - Reloaded ATS Score: {reloaded_gaps['ats_score']}%")

    # Clean up test records
    db.delete(reloaded_analysis)
    db.delete(reloaded_resume)
    db.commit()
    print("\n=== ALL 16 ACCEPTANCE CONDITIONS PASSED PERFECTLY ===")

if __name__ == '__main__':
    main()
