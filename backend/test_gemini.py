import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# Ensure we can load the backend app
sys.path.insert(0, os.path.abspath("."))
load_dotenv(".env")

from app.services.interview_ai import generate_interview_questions

def main():
    print("Running generate_interview_questions for Aptitude...")
    questions = generate_interview_questions(
        company_name="Google",
        role="Software Engineer",
        difficulty="Medium",
        round_title="Aptitude Round",
        count=10
    )
    
    print("\n\n--- RESULTS (FIRST 3 QUESTIONS) ---")
    for idx, q in enumerate(questions[:3]):
        print(f"\n[APTITUDE] Q{idx+1}:")
        print(f"Prompt: {q['prompt']}")
        print(f"Options: {q.get('options')}")
        print(f"Correct: {q.get('correct_answer')}")

if __name__ == "__main__":
    main()
