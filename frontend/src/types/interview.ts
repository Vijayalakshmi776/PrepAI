export interface InterviewRoundInfo {
  id: string;
  order: number;
  title: string;
  description: string | null;
}

export interface InterviewPatternInfo {
  id: string;
  name: string;
  description: string | null;
  rounds: InterviewRoundInfo[];
}

export interface CompanyInfo {
  id: string;
  name: string;
  company_type: string | null;
  difficulty_level: string | null;
  description: string | null;
  patterns: InterviewPatternInfo[];
}

export interface InterviewAnswerInfo {
  id: string;
  response: string;
  score: number | null;
  feedback?: string | null;
}

export interface InterviewQuestionInfo {
  id: string;
  order: number;
  prompt: string;
  question_type?: 'text' | 'mcq';
  options?: string[];
  answer: InterviewAnswerInfo | null;
}

export interface InterviewFeedbackInfo {
  id?: string;
  summary: string;
  strengths: string;
  weaknesses: string;
  recommendations: string;
  overall_score?: number;
}

export interface InterviewSessionSummary {
  id: string;
  title: string;
  completed: boolean;
  created_at: string;
  questions_count: number;
  answers_count: number;
  feedback: InterviewFeedbackInfo | null;
}

export interface InterviewSessionDetail {
  id: string;
  title: string;
  company_name?: string;
  role?: string;
  difficulty?: string;
  round_title?: string;
  completed: boolean;
  created_at: string;
  questions: InterviewQuestionInfo[];
  feedback: InterviewFeedbackInfo | null;
  overall_score?: number;
}
