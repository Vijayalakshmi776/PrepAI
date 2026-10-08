import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.api_v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.company import Company
from app.models.company_interview_pattern import CompanyInterviewPattern
from app.models.interview_round import InterviewRound
from app.models.interview_session import InterviewSession
from app.models.interview_question import InterviewQuestion
from app.models.interview_answer import InterviewAnswer
from app.models.interview_feedback import InterviewFeedback
from app.services.interview_ai import (
    generate_interview_questions,
    evaluate_answer,
    generate_session_summary,
    resolve_round_category,
)

router = APIRouter()

# Default seed data for companies, patterns, and rounds
DEFAULT_COMPANIES = [
    {
        "name": "TCS",
        "company_type": "Service-based",
        "difficulty_level": "Medium",
        "description": "Tata Consultancy Services - Global IT services and consulting leader.",
        "pattern": "TCS National Qualifier & Technical Flow",
        "rounds": [
            {"order": 1, "title": "Round 1: Aptitude", "description": "Quantitative aptitude, numerical ability, and logical reasoning."},
            {"order": 2, "title": "Round 2: Coding", "description": "Hands-on programming, data structures, and algorithmic logic."},
            {"order": 3, "title": "Round 3: Technical", "description": "Core CS fundamentals, OOPs, DBMS, OS, and system architecture."},
            {"order": 4, "title": "Round 4: HR / Behavioral", "description": "Communication, scenario handling, teamwork, and cultural alignment."}
        ]
    },
    {
        "name": "Infosys",
        "company_type": "Service-based",
        "difficulty_level": "Medium",
        "description": "Infosys - Next-generation digital services and consulting.",
        "pattern": "Infosys Specialist Programmer & SE Interview Loop",
        "rounds": [
            {"order": 1, "title": "Round 1: Aptitude & Reasoning", "description": "Quantitative, logical, and verbal reasoning."},
            {"order": 2, "title": "Round 2: Coding & Problem Solving", "description": "Data structures, arrays, strings, searching, and sorting."},
            {"order": 3, "title": "Round 3: Technical Fundamentals", "description": "SQL queries, relational modeling, web architecture, and language concepts."},
            {"order": 4, "title": "Round 4: HR & Behavioral", "description": "Communication skills, career vision, and organizational fit."}
        ]
    },
    {
        "name": "Zoho",
        "company_type": "Product-based",
        "difficulty_level": "Medium-Hard",
        "description": "Zoho Corporation - Premier cloud software and SaaS suite provider.",
        "pattern": "Zoho Software Developer Placement Flow",
        "rounds": [
            {"order": 1, "title": "Round 1: Aptitude & Logic", "description": "Quantitative aptitude, numerical ability, and logical reasoning."},
            {"order": 2, "title": "Round 2: Advanced Coding & Algorithms", "description": "Complex string and matrix problems without high-level library shortcuts."},
            {"order": 3, "title": "Round 3: System Design & Low-Level Architecture", "description": "Designing modular applications (e.g., Taxi Booking, Splitwise, Railway Reservation)."},
            {"order": 4, "title": "Round 4: Technical HR & Logic", "description": "Core computer science problem solving and architectural thinking."}
        ]
    },
    {
        "name": "Google",
        "company_type": "Product-based",
        "difficulty_level": "Difficult",
        "description": "Google - Technology leader in search, cloud, AI, and distributed systems.",
        "pattern": "Google SWE Technical Interview Loop",
        "rounds": [
            {"order": 1, "title": "Round 1: Aptitude & Logic", "description": "Quantitative aptitude, numerical ability, and logical reasoning."},
            {"order": 2, "title": "Round 2: Data Structures & Algorithms (Trees/Graphs)", "description": "Graph traversals, Dynamic Programming, and asymptotic efficiency."},
            {"order": 3, "title": "Round 3: System Design & Scalability", "description": "Large-scale distributed systems, trade-offs, and data pipelines."},
            {"order": 4, "title": "Round 4: Googleyness & Behavioral Leadership", "description": "Navigating ambiguity, collaboration, and ethical engineering judgment."}
        ]
    },
    {
        "name": "Amazon",
        "company_type": "Product-based",
        "difficulty_level": "Difficult",
        "description": "Amazon - Global e-commerce, cloud computing (AWS), and AI innovator.",
        "pattern": "Amazon SDE Interview Process",
        "rounds": [
            {"order": 1, "title": "Round 1: Aptitude & Logic", "description": "Quantitative aptitude, numerical ability, and logical reasoning."},
            {"order": 2, "title": "Round 2: Problem Solving & Data Structures", "description": "Trees, heaps, hashing, and Amazon Leadership Principles integration."},
            {"order": 3, "title": "Round 3: System Design & Scalability", "description": "Low-level and high-level architectural patterns for high-throughput systems."},
            {"order": 4, "title": "Round 4: Bar Raiser & Leadership Principles", "description": "Deep dive on Customer Obsession, Ownership, and Bias for Action."}
        ]
    },
    {
        "name": "Microsoft",
        "company_type": "Product-based",
        "difficulty_level": "Difficult",
        "description": "Microsoft - Cloud, productivity, enterprise software, and AI platform creator.",
        "pattern": "Microsoft SDE Interview Process",
        "rounds": [
            {"order": 1, "title": "Round 1: Aptitude & Logic", "description": "Quantitative aptitude, numerical ability, and logical reasoning."},
            {"order": 2, "title": "Round 2: Data Structures & Core CS", "description": "Linked lists, trees, recursion, OS fundamentals, and memory management."},
            {"order": 3, "title": "Round 3: System Design & Object Modeling", "description": "Designing extensible software modules, APIs, and cloud services."},
            {"order": 4, "title": "Round 4: Hiring Manager & Culture Fit", "description": "Growth mindset, technical curiosity, and collaborative problem solving."}
        ]
    },
    {
        "name": "Startup",
        "company_type": "Startup",
        "difficulty_level": "Medium-Hard",
        "description": "High-velocity tech startups building scalable modern web and AI applications.",
        "pattern": "Fast-Paced Full Stack & Product Engineer Flow",
        "rounds": [
            {"order": 1, "title": "Round 1: Aptitude & Logic", "description": "Quantitative aptitude, numerical ability, and logical reasoning."},
            {"order": 2, "title": "Round 2: Practical Coding & Real-world Problem Solving", "description": "API integration, state management, asynchronous handling, and bug resolution."},
            {"order": 3, "title": "Round 3: System Architecture & Database Design", "description": "Database schema modeling, caching, authentication, and microservice trade-offs."},
            {"order": 4, "title": "Round 4: Founder & Cultural Alignment", "description": "Autonomous execution, ownership, resilience, and speed of delivery."}
        ]
    }
]


def ensure_seeded_companies(db: Session) -> list[Company]:
    """Ensures default company catalog and interview patterns exist and are up to date in PostgreSQL."""
    companies = db.query(Company).all()
    if not companies:
        for c_data in DEFAULT_COMPANIES:
            company = Company(
                name=c_data["name"],
                company_type=c_data["company_type"],
                difficulty_level=c_data["difficulty_level"],
                description=c_data["description"],
            )
            db.add(company)
            db.flush()

            pattern = CompanyInterviewPattern(
                company_id=company.id,
                name=c_data["pattern"],
                description=f"Standard placement and interview roadmap for {company.name}."
            )
            db.add(pattern)
            db.flush()

            for r_data in c_data["rounds"]:
                round_obj = InterviewRound(
                    pattern_id=pattern.id,
                    order=r_data["order"],
                    title=r_data["title"],
                    description=r_data["description"],
                )
                db.add(round_obj)

        db.commit()
        companies = db.query(Company).all()
    else:
        # Sync existing company patterns to guarantee configured 4-round progression
        for c_data in DEFAULT_COMPANIES:
            company = db.query(Company).filter(Company.name.ilike(c_data["name"])).first()
            if company and company.interview_patterns:
                pattern = company.interview_patterns[0]
                existing_rounds = {r.order: r for r in pattern.rounds}
                for r_data in c_data["rounds"]:
                    if r_data["order"] in existing_rounds:
                        r_obj = existing_rounds[r_data["order"]]
                        r_obj.title = r_data["title"]
                        r_obj.description = r_data["description"]
                    else:
                        new_r = InterviewRound(
                            pattern_id=pattern.id,
                            order=r_data["order"],
                            title=r_data["title"],
                            description=r_data["description"],
                        )
                        db.add(new_r)
        db.commit()
        companies = db.query(Company).all()

    return companies


# Schemas for Interview API
class StartSessionRequest(BaseModel):
    company_name: str
    role: str = "Software Engineer"
    difficulty: str = "Medium"
    round_title: Optional[str] = None
    round_id: Optional[str] = None
    company_id: Optional[str] = None


class SubmitAnswerRequest(BaseModel):
    response: str


def format_session_detail(session: InterviewSession, db: Session) -> dict[str, Any]:
    """Helper to serialize full session details with dynamic round sequence and questions."""
    pattern = session.pattern
    if not pattern and session.company and session.company.interview_patterns:
        pattern = session.company.interview_patterns[0]

    sorted_rounds = sorted(pattern.rounds, key=lambda r: r.order) if pattern and pattern.rounds else []
    sorted_questions = sorted(session.questions, key=lambda q: q.order)

    # Determine current round based on latest question in the session
    current_round_obj = None
    if sorted_questions:
        latest_round_id = sorted_questions[-1].round_id
        if latest_round_id:
            current_round_obj = next((r for r in sorted_rounds if r.id == latest_round_id), None)

    if not current_round_obj and sorted_rounds:
        current_round_obj = sorted_rounds[0]

    current_round_order = current_round_obj.order if current_round_obj else 1
    total_rounds = len(sorted_rounds) if sorted_rounds else 1
    current_round_number = 1
    if current_round_obj and sorted_rounds:
        for idx, r in enumerate(sorted_rounds):
            if r.id == current_round_obj.id:
                current_round_number = idx + 1
                break

    rounds_out = []
    for idx, r in enumerate(sorted_rounds):
        round_q_ids = [q.id for q in sorted_questions if q.round_id == r.id]
        round_ans_count = sum(1 for q in sorted_questions if q.round_id == r.id and q.answers)
        is_completed = len(round_q_ids) > 0 and round_ans_count >= len(round_q_ids)
        is_current = (current_round_obj is not None) and (r.id == current_round_obj.id)
        rounds_out.append({
            "id": str(r.id),
            "order": r.order,
            "round_number": idx + 1,
            "title": r.title,
            "description": r.description,
            "questions_count": len(round_q_ids),
            "answers_count": round_ans_count,
            "is_current": is_current,
            "is_completed": is_completed,
        })

    questions_out = []
    for q in sorted_questions:
        ans = q.answers[0] if q.answers else None
        questions_out.append({
            "id": str(q.id),
            "order": q.order,
            "round_id": str(q.round_id) if q.round_id else None,
            "round_title": q.round.title if q.round else None,
            "round_order": q.round.order if q.round else 1,
            "prompt": q.prompt,
            "question_type": q.question_type,
            "options": q.options,
            "correct_answer": q.correct_answer,
            "answer": {
                "id": str(ans.id),
                "response": ans.response,
                "score": ans.score,
            } if ans else None
        })

    feedback_obj = session.feedback[0] if session.feedback else None
    company_name = session.company.name if session.company else "Company"

    current_round_dict = None
    if current_round_obj:
        current_round_dict = {
            "id": str(current_round_obj.id),
            "order": current_round_obj.order,
            "round_number": current_round_number,
            "total_rounds": total_rounds,
            "title": current_round_obj.title,
            "description": current_round_obj.description,
        }

    return {
        "id": str(session.id),
        "title": session.title,
        "company_name": company_name,
        "role": getattr(session, 'role', 'Software Engineer') or "Software Engineer",
        "difficulty": getattr(session, 'difficulty', 'Medium') or "Medium",
        "completed": session.completed,
        "created_at": session.created_at.isoformat(),
        "pattern_id": str(pattern.id) if pattern else None,
        "pattern_name": pattern.name if pattern else None,
        "current_round": current_round_dict,
        "rounds": rounds_out,
        "questions": questions_out,
        "feedback": {
            "id": str(feedback_obj.id),
            "summary": feedback_obj.summary,
            "strengths": feedback_obj.strengths,
            "weaknesses": feedback_obj.weaknesses,
            "recommendations": feedback_obj.recommendations,
            "overall_score": getattr(feedback_obj, 'overall_score', None)
        } if feedback_obj else None
    }


@router.get('/companies')
def get_companies(db: Session = Depends(get_db)):
    """Return all available companies with their interview patterns and rounds."""
    companies = ensure_seeded_companies(db)
    result = []
    for c in companies:
        patterns = []
        for p in c.interview_patterns:
            rounds = [
                {"id": str(r.id), "order": r.order, "title": r.title, "description": r.description}
                for r in sorted(p.rounds, key=lambda x: x.order)
            ]
            patterns.append({"id": str(p.id), "name": p.name, "description": p.description, "rounds": rounds})
        result.append({
            "id": str(c.id),
            "name": c.name,
            "company_type": c.company_type,
            "difficulty_level": c.difficulty_level,
            "description": c.description,
            "patterns": patterns,
        })
    return result


@router.post('/sessions')
def start_interview_session(
    payload: StartSessionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Creates a new Mock Interview session in PostgreSQL and starts strictly from the FIRST configured round.
    """
    ensure_seeded_companies(db)
    user_id = current_user.id

    # Lookup Company
    company = db.query(Company).filter(Company.name.ilike(payload.company_name.strip())).first()
    pattern = None
    pattern_id = None
    company_id = None
    if company:
        company_id = company.id
        if company.interview_patterns:
            pattern = company.interview_patterns[0]
            pattern_id = pattern.id

    # Strictly determine the FIRST configured interview round for this pattern
    sorted_rounds = sorted(pattern.rounds, key=lambda r: r.order) if pattern and pattern.rounds else []
    
    selected_round = sorted_rounds[0] if sorted_rounds else None

    round_title = selected_round.title if selected_round else 'Round 1: Technical'
    round_id = selected_round.id if selected_round else None

    title = f"{payload.company_name} - {round_title} ({payload.role})"

    session = InterviewSession(
        user_id=user_id,
        company_id=company_id,
        pattern_id=pattern_id,
        title=title,
        role=payload.role,
        difficulty=payload.difficulty,
        completed=False,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # Generate questions tailored to the FIRST configured round
    category = resolve_round_category(round_title)
    q_count = 10 if category == "Aptitude" else 3

    prompts = generate_interview_questions(
        company_name=payload.company_name,
        role=payload.role,
        difficulty=payload.difficulty,
        round_title=round_title,
        count=q_count
    )

    for index, q_dict in enumerate(prompts):
        question = InterviewQuestion(
            session_id=session.id,
            round_id=round_id,
            prompt=q_dict.get("prompt", ""),
            question_type=q_dict.get("question_type", "text"),
            options=q_dict.get("options"),
            correct_answer=q_dict.get("correct_answer"),
            order=index + 1,
        )
        db.add(question)

    db.commit()
    db.refresh(session)

    return format_session_detail(session, db)


@router.post('/sessions/{session_id}/next-round')
def advance_to_next_round(
    session_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Advances an active mock interview session to the NEXT sequential round defined in the pattern.
    Generates questions for that round and updates session state.
    """
    try:
        s_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format.")

    session = db.query(InterviewSession).filter(
        InterviewSession.id == s_uuid,
        InterviewSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    if session.completed:
        raise HTTPException(status_code=400, detail="Interview session is already completed.")

    pattern = session.pattern
    if not pattern and session.company and session.company.interview_patterns:
        pattern = session.company.interview_patterns[0]

    if not pattern or not pattern.rounds:
        raise HTTPException(status_code=400, detail="No interview pattern configured for this company.")

    sorted_rounds = sorted(pattern.rounds, key=lambda r: r.order)
    sorted_questions = sorted(session.questions, key=lambda q: q.order)

    # Identify current round
    current_round_obj = None
    if sorted_questions:
        latest_round_id = sorted_questions[-1].round_id
        if latest_round_id:
            current_round_obj = next((r for r in sorted_rounds if r.id == latest_round_id), None)

    current_idx = 0
    if current_round_obj:
        for idx, r in enumerate(sorted_rounds):
            if r.id == current_round_obj.id:
                current_idx = idx
                break

    next_idx = current_idx + 1
    if next_idx >= len(sorted_rounds):
        # All configured rounds are finished -> complete the session
        return complete_interview_session(session_id=session_id, db=db, current_user=current_user)

    next_round = sorted_rounds[next_idx]
    company_name = session.company.name if session.company else "Company"
    sess_role = getattr(session, 'role', 'Software Engineer') or 'Software Engineer'
    sess_diff = getattr(session, 'difficulty', 'Medium') or 'Medium'

    # Generate questions for the next round
    category = resolve_round_category(next_round.title)
    q_count = 10 if category == "Aptitude" else 3

    prompts = generate_interview_questions(
        company_name=company_name,
        role=sess_role,
        difficulty=sess_diff,
        round_title=next_round.title,
        count=q_count
    )

    base_order = len(sorted_questions)
    for idx, q_dict in enumerate(prompts):
        question = InterviewQuestion(
            session_id=session.id,
            round_id=next_round.id,
            prompt=q_dict.get("prompt", ""),
            question_type=q_dict.get("question_type", "text"),
            options=q_dict.get("options"),
            correct_answer=q_dict.get("correct_answer"),
            order=base_order + idx + 1,
        )
        db.add(question)

    session.title = f"{company_name} - {next_round.title} ({sess_role})"
    db.add(session)
    db.commit()
    db.refresh(session)

    return format_session_detail(session, db)


@router.get('/sessions')
def list_user_sessions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List all mock interview sessions for the current user."""
    sessions = (
        db.query(InterviewSession)
        .filter(InterviewSession.user_id == current_user.id)
        .order_by(InterviewSession.created_at.desc())
        .all()
    )
    result = []
    for s in sessions:
        feedback_obj = s.feedback[0] if s.feedback else None
        answers_count = sum(len(q.answers) for q in s.questions)
        result.append({
            "id": str(s.id),
            "title": s.title,
            "completed": s.completed,
            "created_at": s.created_at.isoformat(),
            "questions_count": len(s.questions),
            "answers_count": answers_count,
            "feedback": {
                "summary": feedback_obj.summary,
                "strengths": feedback_obj.strengths,
                "weaknesses": feedback_obj.weaknesses,
                "recommendations": feedback_obj.recommendations
            } if feedback_obj else None
        })
    return result


@router.get('/sessions/{session_id}')
def get_interview_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Retrieve full details of a mock interview session including questions, answers, and feedback."""
    try:
        s_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format.")

    session = db.query(InterviewSession).filter(
        InterviewSession.id == s_uuid,
        InterviewSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    return format_session_detail(session, db)


@router.post('/questions/{question_id}/answer')
def submit_question_answer(
    question_id: str,
    payload: SubmitAnswerRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Submits and evaluates an answer for an interview question.
    Persists the answer and score in PostgreSQL.
    """
    try:
        q_uuid = uuid.UUID(question_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid question ID format.")

    question = db.query(InterviewQuestion).filter(InterviewQuestion.id == q_uuid).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    session = question.session
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to answer this question.")

    # Evaluate answer using AI reasoning engine
    company_name = session.company.name if session.company else "Company"
    score, feedback_text = evaluate_answer(
        question_prompt=question.prompt,
        user_response=payload.response,
        company_name=company_name,
        role="Software Engineer",
        difficulty="Medium",
        round_title=question.round.title if question.round else None,
        question_type=question.question_type,
        correct_answer=question.correct_answer
    )

    # Persist or update InterviewAnswer
    existing_answer = db.query(InterviewAnswer).filter(
        InterviewAnswer.question_id == question.id,
        InterviewAnswer.user_id == current_user.id
    ).first()

    if existing_answer:
        existing_answer.response = payload.response
        existing_answer.score = score
        db.add(existing_answer)
        answer_id = str(existing_answer.id)
    else:
        new_answer = InterviewAnswer(
            question_id=question.id,
            user_id=current_user.id,
            response=payload.response,
            score=score
        )
        db.add(new_answer)
        db.flush()
        answer_id = str(new_answer.id)

    db.commit()

    return {
        "answer_id": answer_id,
        "question_id": str(question.id),
        "score": score,
        "feedback": feedback_text,
        "response": payload.response,
    }


@router.post('/sessions/{session_id}/complete')
def complete_interview_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Completes the mock interview session, generates comprehensive feedback across all rounds,
    and saves InterviewFeedback in PostgreSQL.
    """
    try:
        s_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format.")

    session = db.query(InterviewSession).filter(
        InterviewSession.id == s_uuid,
        InterviewSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    # Gather Q&A across all rounds for summary
    qa_list = []
    for q in sorted(session.questions, key=lambda x: x.order):
        score = 0
        response_text = ""
        if q.answers:
            ans = q.answers[0]
            score = ans.score or 0
            response_text = ans.response
            
        qa_list.append({
            "prompt": q.prompt,
            "response": response_text,
            "score": score,
            "round_title": q.round.title if q.round else None,
            "question_type": q.question_type
        })

    company_name = session.company.name if session.company else "Company"
    summary_data = generate_session_summary(
        session_title=session.title,
        company_name=company_name,
        role="Software Engineer",
        questions_and_answers=qa_list
    )

    # Save InterviewFeedback in PostgreSQL
    feedback = db.query(InterviewFeedback).filter(InterviewFeedback.session_id == session.id).first()
    if not feedback:
        feedback = InterviewFeedback(
            session_id=session.id,
            summary=summary_data["summary"],
            strengths=summary_data["strengths"],
            weaknesses=summary_data["weaknesses"],
            recommendations=summary_data["recommendations"]
        )
        db.add(feedback)
    else:
        feedback.summary = summary_data["summary"]
        feedback.strengths = summary_data["strengths"]
        feedback.weaknesses = summary_data["weaknesses"]
        feedback.recommendations = summary_data["recommendations"]
        db.add(feedback)

    session.completed = True
    db.add(session)
    db.commit()
    db.refresh(feedback)

    return {
        "session_id": str(session.id),
        "completed": True,
        "overall_score": summary_data["overall_score"],
        "summary": feedback.summary,
        "strengths": feedback.strengths,
        "weaknesses": feedback.weaknesses,
        "recommendations": feedback.recommendations
    }
