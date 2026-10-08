import asyncio
import json
from app.services.interview_ai import generate_interview_questions

def main():
    questions = generate_interview_questions(
        company_name="Startup",
        role="Software Engineer",
        difficulty="Medium",
        round_title="Round 1: Aptitude & Logic",
        count=10
    )
    print(json.dumps(questions, indent=2))

if __name__ == "__main__":
    main()
