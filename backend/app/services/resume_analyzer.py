import io
import json
import logging
import re
import time
import unicodedata
from typing import Any
import httpx
from pypdf import PdfReader
from app.core.config import settings

logger = logging.getLogger(__name__)

# Comprehensive Technical Skill Catalog (c and r handled with strict context)
SKILL_TAXONOMY: dict[str, list[str]] = {
    "Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "golang",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "sql", "html", "css", "bash", "shell"
    ],
    "Frameworks & Web": [
        "react", "react.js", "next.js", "vue", "vue.js", "angular", "node.js", "express", "express.js",
        "django", "fastapi", "flask", "spring boot", "spring", "asp.net", ".net", "tailwind", "tailwindcss",
        "bootstrap", "graphql", "rest api", "rest apis", "restful", "redux", "websockets",
        "state management", "responsive design", "accessibility", "a11y"
    ],
    "Databases & Storage": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "sqlite", "oracle",
        "cassandra", "dynamodb", "elasticsearch", "firebase", "mariadb", "neo4j", "database", "databases"
    ],
    "Cloud, DevOps & Tools": [
        "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s",
        "ci/cd", "git", "github", "gitlab", "linux", "unix", "terraform", "jenkins", "nginx", "postman",
        "deployment", "authentication", "backend architecture"
    ],
    "CS Fundamentals & AI/ML": [
        "data structures", "algorithms", "dsa", "system design", "object-oriented programming", "oops",
        "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
        "scikit-learn", "pandas", "numpy", "microservices", "unit testing", "testing", "agile", "scrum",
        "statistics", "data processing", "model evaluation", "data visualization"
    ]
}

# Role-specific essential skill profiles
ROLE_REQUIREMENTS: dict[str, list[str]] = {
    "frontend developer": [
        "HTML", "CSS", "JavaScript", "TypeScript", "React", "State Management",
        "REST APIs", "Git", "Responsive Design", "Accessibility", "Testing"
    ],
    "react developer": [
        "HTML", "CSS", "JavaScript", "React", "State Management", "REST APIs", "Git", "TypeScript", "Testing"
    ],
    "ui developer": [
        "HTML", "CSS", "JavaScript", "React", "Responsive Design", "Accessibility", "Git"
    ],
    "backend developer": [
        "Python", "Node.js", "Java", "REST APIs", "Databases", "PostgreSQL", "SQL",
        "Authentication", "Testing", "Backend Architecture", "Deployment", "Docker"
    ],
    "full stack developer": [
        "Frontend", "Backend", "Database", "REST APIs", "Authentication", "Git",
        "Deployment", "JavaScript", "React", "Node.js", "SQL"
    ],
    "ai/ml engineer": [
        "Python", "Machine Learning", "Statistics", "Data Processing", "Model Evaluation",
        "NumPy", "Pandas", "Scikit-Learn", "Deep Learning", "TensorFlow", "PyTorch"
    ],
    "software engineer": [
        "Python", "Java", "Data Structures", "Algorithms", "SQL", "Git", "System Design",
        "REST APIs", "C++", "Testing"
    ],
    "data engineer": [
        "Python", "SQL", "PostgreSQL", "AWS", "Docker", "Pandas", "Data Structures", "Git", "ETL", "Spark", "Hadoop"
    ],
    "data scientist": [
        "Python", "Machine Learning", "Pandas", "NumPy", "SQL", "Scikit-Learn", "Statistics", "Data Visualization"
    ],
    "cloud / devops engineer": [
        "AWS", "Docker", "Kubernetes", "Linux", "CI/CD", "Terraform", "Git", "Python", "Networking", "Security"
    ],
    "cybersecurity engineer": [
        "Security", "Linux", "Networking", "Python", "Penetration Testing", "Cryptography", "Firewalls"
    ],
}

ACTION_VERBS = [
    "architected", "engineered", "developed", "built", "spearheaded", "designed",
    "implemented", "optimized", "reduced", "accelerated", "automated", "streamlined",
    "scaled", "enhanced", "orchestrated", "deployed", "refactored", "migrated"
]


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        extracted_pages = []
        for i, page in enumerate(reader.pages):
            txt = page.extract_text()
            if txt:
                extracted_pages.append(txt)
        raw_text = "\n".join(extracted_pages).strip()
        if raw_text:
            # 1. Unicode normalization (NFKC)
            norm = unicodedata.normalize("NFKC", raw_text)
            # 2. Strip non-printable control characters (preserving \n and \t)
            norm = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", norm)
            # 3. Replace non-standard whitespace characters
            norm = norm.replace("\xa0", " ").replace("\u200b", "").replace("\r\n", "\n").replace("\r", "\n")
            # 4. Clean line spacing without breaking tech tokens or words
            lines = [re.sub(r"[ \t]+", " ", line).strip() for line in norm.split("\n")]
            cleaned_text = "\n".join(lines).strip()
            cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)
            
            words = re.findall(r"\b[\w+#\.]+\b", cleaned_text)
            logger.info(
                f"PDF Text Extraction Diagnostic: pages={len(reader.pages)}, "
                f"extracted_characters={len(cleaned_text)}, extracted_words={len(words)}"
            )
            return cleaned_text
    except Exception as e:
        logger.warning(f"pypdf extraction failed: {e}")
    return ""


def detect_skills_in_text(text: str) -> list[str]:
    if not text or not text.strip():
        return []

    lower_text = text.lower()
    detected: set[str] = set()

    def match_token(pattern_str: str) -> bool:
        # Negative lookbehind and lookahead for alphanumeric, +, #
        pat = rf"(?<![a-zA-Z0-9#+]){pattern_str}(?![a-zA-Z0-9#+])"
        return bool(re.search(pat, lower_text, re.IGNORECASE))

    # Comprehensive skill pattern mappings (Clean Display Name -> Pattern)
    SKILL_PATTERNS: list[tuple[str, str]] = [
        ("HTML", r"(?:html5?|html)"),
        ("CSS", r"(?:css3?|css)"),
        ("JavaScript", r"(?:javascript|java\s+script|\bjs\b)"),
        ("TypeScript", r"(?:typescript|\bts\b)"),
        ("React", r"(?:react(?:\.js|js)?|react)"),
        ("Node.js", r"(?:node(?:\.js|js)?|nodejs)"),
        ("Next.js", r"(?:next(?:\.js|js)?|nextjs)"),
        ("Vue.js", r"(?:vue(?:\.js|js)?|vuejs)"),
        ("Express.js", r"(?:express(?:\.js|js)?|expressjs)"),
        ("FastAPI", r"fastapi"),
        ("Flask", r"flask"),
        ("Django", r"django"),
        ("Spring Boot", r"(?:spring\s+boot|spring)"),
        (".NET", r"(?:asp\.net|\.net)"),
        ("Tailwind CSS", r"(?:tailwind|tailwindcss)"),
        ("Bootstrap", r"bootstrap"),
        ("GraphQL", r"graphql"),
        ("REST APIs", r"(?:rest\s*apis?|restful|rest\s+api)"),
        ("Redux", r"redux"),
        ("WebSockets", r"websockets?"),
        ("Python", r"python"),
        ("Java", r"java"),
        ("C++", r"(?:c\+\+|cpp)"),
        ("C#", r"(?:c#|csharp)"),
        ("Go", r"(?:golang|go)"),
        ("Rust", r"rust"),
        ("Ruby", r"ruby"),
        ("PHP", r"php"),
        ("Swift", r"swift"),
        ("Kotlin", r"kotlin"),
        ("Scala", r"scala"),
        ("SQL", r"sql"),
        ("PostgreSQL", r"(?:postgresql|postgres)"),
        ("MySQL", r"mysql"),
        ("MongoDB", r"mongodb"),
        ("Redis", r"redis"),
        ("SQLite", r"sqlite"),
        ("Oracle", r"oracle"),
        ("Firebase", r"firebase"),
        ("AWS", r"(?:aws|amazon\s+web\s+services)"),
        ("GCP", r"(?:gcp|google\s+cloud)"),
        ("Azure", r"azure"),
        ("Docker", r"docker"),
        ("Kubernetes", r"(?:kubernetes|k8s)"),
        ("CI/CD", r"ci\s*/\s*cd"),
        ("Git", r"git"),
        ("GitHub", r"github"),
        ("GitLab", r"gitlab"),
        ("Linux", r"linux"),
        ("Unix", r"unix"),
        ("Terraform", r"terraform"),
        ("Jenkins", r"jenkins"),
        ("Nginx", r"nginx"),
        ("Postman", r"postman"),
        ("Data Structures", r"(?:data\s+structures|dsa)"),
        ("Algorithms", r"algorithms?"),
        ("System Design", r"system\s+design"),
        ("Machine Learning", r"(?:machine\s+learning|\bml\b)"),
        ("Deep Learning", r"deep\s+learning"),
        ("NLP", r"nlp"),
        ("TensorFlow", r"tensorflow"),
        ("PyTorch", r"pytorch"),
        ("Scikit-Learn", r"(?:scikit-learn|scikit\s+learn|sklearn)"),
        ("Pandas", r"pandas"),
        ("NumPy", r"numpy"),
        ("State Management", r"state\s+management"),
        ("Responsive Design", r"responsive\s+design"),
        ("Accessibility", r"(?:accessibility|a11y)"),
        ("Testing", r"(?:unit\s+testing|integration\s+testing|testing)"),
        ("Authentication", r"authentication"),
        ("Backend Architecture", r"backend\s+architecture"),
        ("Data Processing", r"data\s+processing"),
        ("Model Evaluation", r"model\s+evaluation"),
        ("Data Visualization", r"data\s+visualization")
    ]

    for name, pattern in SKILL_PATTERNS:
        if match_token(pattern):
            detected.add(name)

    # Contextual check for single-letter skills C and R (require explicit language/programming context)
    if re.search(r"\b(?:c\s+programming|c\s+language|c\s*/\s*c\+\+|languages?\s*:\s*[^;\n]*?\bc\b|skills?\s*:\s*[^;\n]*?\bc\b)", lower_text):
        detected.add("C")
    if re.search(r"\b(?:r\s+programming|r\s+language|r\s+studio|rstudio|languages?\s*:\s*[^;\n]*?\br\b|skills?\s*:\s*[^;\n]*?\br\b)", lower_text):
        detected.add("R")

    # Additional high-level domain indicators
    if any(k in lower_text for k in ["frontend", "web design", "ui/ux", "dom", "html5", "css3"]):
        detected.add("Frontend")
    if any(k in lower_text for k in ["backend", "server-side", "api development", "microservices"]):
        detected.add("Backend")
    if any(k in lower_text for k in ["database", "dbms", "sql query", "relational database"]):
        detected.add("Database")

    return sorted(list(detected))

def call_gemini_resume_analysis(resume_text: str, target_role: str, target_company: str, detected_skills: list[str], missing_skills: list[str]) -> dict[str, Any]:
    prompt = f"""You are a principal tech recruiter evaluating a candidate resume for {target_company} ({target_role}).
    
Resume Text:
{resume_text[:3500]}

Detected Skills from Text: {', '.join(detected_skills)}
Missing Core Skills for {target_role}: {', '.join(missing_skills)}

CRITICAL ANTI-HALLUCINATION & EVALUATION RULES:
1. DO NOT claim the candidate has a skill unless there is factual evidence in the resume text.
2. The `job_role_recommendations` MUST ONLY include roles that strongly match the candidate's extracted skills (minimum 55% evidence match).
3. Do NOT recommend completely unrelated domains (e.g. Data Scientist, DevOps Engineer, Cybersecurity Engineer for a candidate with only Web/Frontend skills).
4. For every recommended role, provide exact matching skills, missing skills, and an explainable reason referencing extracted resume evidence.
5. If no alternative roles meet the 55% threshold, return an empty array [] for `job_role_recommendations`.

Return ONLY a valid JSON object analyzing this resume. DO NOT include markdown formatting or backticks.
Schema:
{{
  "extracted_name": "Name or null",
  "extracted_email": "Email or null",
  "extracted_phone": "Phone or null",
  "extracted_education": ["Degree 1"],
  "extracted_experience": ["Job 1"],
  "extracted_projects": ["Project 1"],
  "extracted_soft_skills": ["Communication"],
  "extracted_certifications": [],
  "extracted_achievements": [],
  "missing_keywords": ["Keyword1"],
  "formatting_issues": [],
  "content_improvements": ["Improvement 1"],
  "project_improvements": ["Proj Improvement 1"],
  "experience_improvements": ["Exp Improvement 1"],
  "strengths": ["Strength 1"],
  "weaknesses": ["Weakness 1"],
  "recommendations": ["Recommendation 1"],
  "role_suitability_explanation": "Detailed 2-3 sentence explanation of suitability for target_role referencing extracted resume evidence.",
  "before_after_suggestions": [
    {{"original_text": "Original bullet", "improved_text": "Improved bullet with metrics", "reason": "Added quantifiable impact"}}
  ],
  "job_role_recommendations": [
    {{"role": "Role Name", "match_percentage": 85.0, "matching_skills": ["HTML", "CSS", "React"], "missing_skills": ["TypeScript"], "reason": "Your resume demonstrates strong frontend experience through HTML, CSS, JavaScript, React and web projects."}}
  ]
}}"""
    
    model_name = "gemini-3.6-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "response_mime_type": "application/json"}
    }
    
    for attempt in range(2):
        try:
            with httpx.Client(timeout=12.0) as client:
                res = client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    raw_llm = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    if "```json" in raw_llm:
                        raw_llm = raw_llm.split("```json")[1].split("```")[0].strip()
                    elif "```" in raw_llm:
                        raw_llm = raw_llm.split("```")[1].split("```")[0].strip()
                    return json.loads(raw_llm)
                else:
                    logger.warning(f"Gemini API Error {res.status_code}: {res.text}")
                    if attempt < 1:
                        time.sleep(1.0)
        except Exception as e:
            logger.warning(f"Gemini API attempt failed: {e}")
            if attempt < 1:
                time.sleep(1.0)
        
    raise Exception("Gemini API fallback triggered")

def analyze_resume_content(
    resume_text: str,
    target_role: str = "Software Engineer",
    target_company: str = "Tech Company",
    career_goal: str = "Placement",
    current_level: str = "Intermediate",
    onboarding_skills: list[str] | None = None,
    roadmap_skill_gaps: list[str] | None = None
) -> dict[str, Any]:
    
    word_count = len(re.findall(r"\b[\w+#\.]+\b", resume_text))
    lower_text = resume_text.lower()
    
    # 1. Skill Detection
    detected_skills = detect_skills_in_text(resume_text)
    detected_lower = {s.lower() for s in detected_skills}
    
    # Match target role key in requirements catalog
    matched_role_key = "software engineer"
    t_role_lower = target_role.lower()
    for r_key in ROLE_REQUIREMENTS:
        if r_key in t_role_lower or t_role_lower in r_key:
            matched_role_key = r_key
            break
            
    required_skills = ROLE_REQUIREMENTS.get(matched_role_key, ROLE_REQUIREMENTS["software engineer"])
    matching_skills = [req for req in required_skills if req.lower() in detected_lower]
    missing_skills = [req for req in required_skills if req.lower() not in detected_lower]
    
    # 2. Deterministic Scoring for Selected Role
    # A. Technical Skill Match (weight 45%)
    total_req = max(len(required_skills), 1)
    matched_req = len(matching_skills)
    skill_match_pct = (matched_req / total_req) * 100
    
    # B. Formatting & Structure (weight 15%)
    formatting_score = 60.0
    has_email = bool(re.search(r"[\w\.-]+@[\w\.-]+\.\w+", resume_text))
    has_phone = bool(re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", resume_text))
    has_links = bool(re.search(r"(github|linkedin|portfolio|\.com|\.dev|\.io)", lower_text))
    
    if has_email: formatting_score += 15
    if has_phone: formatting_score += 10
    if has_links: formatting_score += 15
    if 200 <= word_count <= 900: formatting_score += 20
    elif word_count < 100 or word_count > 1500: formatting_score -= 20
    formatting_score = min(max(formatting_score, 0), 100)
    
    # C. Project & Experience Evidence (weight 25%)
    action_verb_count = sum(1 for verb in ACTION_VERBS if re.search(rf"\b{verb}\b", lower_text))
    metric_count = len(re.findall(r"(\d+[\%xX]|\$\d+|\d+\+?\s*(users|requests|ms|seconds|minutes|hours|days|clients|queries))", resume_text, re.IGNORECASE))
    
    experience_score = min(40 + (action_verb_count * 5), 100)
    project_score = min(40 + (metric_count * 10), 100)
    
    # D. Keyword Match Score (weight 15%)
    company_keywords = target_company.lower().split()
    keyword_matches = sum(1 for kw in company_keywords if kw in lower_text)
    keyword_match_score = min(50 + (keyword_matches * 10) + (len(detected_skills) * 2), 100)
    
    # Education
    education_score = 100.0 if any(ed in lower_text for ed in ["bachelor", "master", "phd", "university", "college", "b.tech", "bsc", "b.s."]) else 50.0

    # Role Suitability Score (0-100) for selected role
    role_suitability_score = round(
        (skill_match_pct * 0.45) +
        (experience_score * 0.15) +
        (project_score * 0.15) +
        (keyword_match_score * 0.15) +
        (formatting_score * 0.10),
        1
    )
    role_suitability_score = min(max(role_suitability_score, 0.0), 100.0)

    # Determine status label
    if role_suitability_score >= 80.0:
        role_suitability_status = "Strong Match"
    elif role_suitability_score >= 70.0:
        role_suitability_status = "Good Match"
    elif role_suitability_score >= 50.0:
        role_suitability_status = "Partial Match"
    else:
        role_suitability_status = "Low Match"

    # Transparent 7-factor PrepAI ATS Compatibility Score calculation
    has_achievements = 100.0 if metric_count >= 1 else 40.0
    ats_score = round(
        (skill_match_pct * 0.25) +
        (keyword_match_score * 0.20) +
        (experience_score * 0.15) +
        (project_score * 0.15) +
        (education_score * 0.10) +
        (formatting_score * 0.10) +
        (has_achievements * 0.05),
        1
    )
    ats_score = min(max(ats_score, 0.0), 100.0)

    # 3. Grounded Job Role Recommendations (Evidence-Based, Threshold >= 55%)
    deterministic_jobs = []
    roles_requiring_prep = []
    for role_key, req_skills in ROLE_REQUIREMENTS.items():
        matched_for_role = [s for s in req_skills if s.lower() in detected_lower]
        missing_for_role = [s for s in req_skills if s.lower() not in detected_lower]
        
        # Check factual match ratio for this role
        raw_match_pct = (len(matched_for_role) / max(len(req_skills), 1)) * 100.0
        final_role_match = (raw_match_pct * 0.75) + (ats_score * 0.25)
        
        display_title = role_key.title()
        if role_key == "ai/ml engineer": display_title = "AI/ML Engineer"
        elif role_key == "full stack developer": display_title = "Full Stack Developer"
        elif role_key == "ui developer": display_title = "UI Developer"

        # Strict anti-hallucination: candidate MUST have matching skills OR >= 55% match
        if final_role_match >= 55.0 and len(matched_for_role) >= 2:
            reasons_str = f"Your resume demonstrates extracted evidence for {', '.join(matched_for_role[:4])}."
            deterministic_jobs.append({
                "role": display_title,
                "match_percentage": round(final_role_match, 1),
                "matching_skills": matched_for_role,
                "missing_skills": missing_for_role[:3],
                "reason": reasons_str
            })
        elif 40.0 <= final_role_match < 55.0 and len(matched_for_role) >= 1:
            roles_requiring_prep.append({
                "role": display_title,
                "match_percentage": round(final_role_match, 1),
                "matching_skills": matched_for_role,
                "missing_skills": missing_for_role[:4],
                "reason": f"Requires additional foundational skills in {', '.join(missing_for_role[:3])} before applying."
            })
            
    # Sort descending by match percentage
    deterministic_jobs = sorted(deterministic_jobs, key=lambda x: x["match_percentage"], reverse=True)[:4]
    roles_requiring_prep = sorted(roles_requiring_prep, key=lambda x: x["match_percentage"], reverse=True)[:3]

    # Generate explanatory text grounded in resume evidence
    if matching_skills:
        explanation_text = f"Your resume demonstrates strong competency in {', '.join(matching_skills[:4])} for {target_role}. Adding {', '.join(missing_skills[:3]) if missing_skills else 'further advanced projects'} would improve your overall fit."
    else:
        explanation_text = f"Your current resume shows limited direct alignment with core skills required for {target_role}. Focusing on acquiring {', '.join(missing_skills[:3])} is highly recommended."

    # Grounded bullet point improvement suggestions
    before_after_suggestions = []
    if matching_skills:
        first_skill = matching_skills[0]
        before_after_suggestions.append({
            "original_text": f"Worked on {first_skill} features for project.",
            "improved_text": f"Engineered key web components using {first_skill}, optimizing interface responsiveness and user experience.",
            "reason": "Uses strong technical action verbs to demonstrate impact."
        })
    if len(matching_skills) >= 2:
        second_skill = matching_skills[1]
        before_after_suggestions.append({
            "original_text": f"Used {second_skill} in software tasks.",
            "improved_text": f"Implemented scalable backend architecture and services using {second_skill}, improving query efficiency.",
            "reason": "Quantifies technical scope and optimization results."
        })

    # Initial response dictionary with fallback status
    response_data = {
        "readiness_score": role_suitability_score,
        "ats_score": ats_score,
        "overall_score": role_suitability_score,
        "role_suitability_score": role_suitability_score,
        "role_suitability_status": role_suitability_status,
        "keyword_match_score": round(keyword_match_score, 1),
        "skills_score": round(skill_match_pct, 1),
        "experience_score": round(experience_score, 1),
        "project_score": round(project_score, 1),
        "education_score": round(education_score, 1),
        "formatting_score": round(formatting_score, 1),
        
        "detected_skills": detected_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "target_role": target_role,
        "target_company": target_company,
        "word_count": word_count,
        
        "gemini_used": False,
        "fallback_used": True,
        "ai_personalization_used": False,
        
        "extracted_name": None, "extracted_email": None, "extracted_phone": None,
        "extracted_education": [], "extracted_experience": [], "extracted_projects": [],
        "extracted_technical_skills": detected_skills, "extracted_soft_skills": [],
        "extracted_certifications": [], "extracted_achievements": [], "extracted_links": [],
        
        "missing_keywords": missing_skills, "formatting_issues": [],
        "content_improvements": [], "project_improvements": [], "experience_improvements": [],
        "strengths": [f"Extracted {len(detected_skills)} verified technical skills from resume"],
        "weaknesses": [f"Missing key role requirement: {s}" for s in missing_skills[:3]],
        "recommendations": [f"Add a project demonstrating {s} to strengthen your resume" for s in missing_skills[:3]] or ["Add more quantifiable metrics"],
        "role_suitability_explanation": explanation_text,
        "before_after_suggestions": before_after_suggestions,
        "job_role_recommendations": deterministic_jobs,
        "roles_requiring_preparation": roles_requiring_prep
    }
    
    # 4. Gemini AI Call for Personalization & Strict Filtering
    has_gemini_key = bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "replace-with-gemini-key")
    logger.info(f"Gemini API configured: {has_gemini_key}")
    if has_gemini_key:
        try:
            ai_data = call_gemini_resume_analysis(resume_text, target_role, target_company, detected_skills, missing_skills)
            
            # Merge AI data safely
            for k in ["extracted_name", "extracted_email", "extracted_phone", "extracted_education", "extracted_experience", 
                     "extracted_projects", "extracted_soft_skills", "extracted_certifications", "extracted_achievements", 
                     "missing_keywords", "formatting_issues", "content_improvements", "project_improvements", 
                     "experience_improvements", "strengths", "weaknesses", "recommendations", "role_suitability_explanation", "before_after_suggestions"]:
                if k in ai_data and ai_data[k]:
                    response_data[k] = ai_data[k]
                    
            # Strict Anti-Hallucination filter on AI job recommendations
            if "job_role_recommendations" in ai_data and isinstance(ai_data["job_role_recommendations"], list):
                valid_ai_jobs = []
                for j in ai_data["job_role_recommendations"]:
                    m_pct = j.get("match_percentage", 0.0)
                    m_skills = j.get("matching_skills", [])
                    # Verify matching skills exist in detected_skills
                    valid_matching = [s for s in m_skills if s.lower() in detected_lower]
                    if m_pct >= 55.0 and len(valid_matching) >= 1:
                        j["matching_skills"] = valid_matching
                        valid_ai_jobs.append(j)
                if valid_ai_jobs:
                    response_data["job_role_recommendations"] = valid_ai_jobs
                elif deterministic_jobs:
                    response_data["job_role_recommendations"] = deterministic_jobs
                    
            response_data["gemini_used"] = True
            response_data["fallback_used"] = False
            response_data["ai_personalization_used"] = True
            response_data["summary"] = f"Evidence-based AI evaluation for '{target_role}' at '{target_company}' completed successfully."
            
        except Exception as e:
            logger.warning(f"AI Personalization fallback triggered: {e}")
            response_data["gemini_used"] = False
            response_data["fallback_used"] = True
            response_data["summary"] = f"Deterministic evaluation for '{target_role}' at '{target_company}'. (AI fallback active)"
    else:
        response_data["summary"] = f"Deterministic evaluation for '{target_role}' at '{target_company}'. (AI key unconfigured)"

    return response_data

