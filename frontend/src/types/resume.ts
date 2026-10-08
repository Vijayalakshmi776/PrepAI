export interface ResumeItem {
  id: string;
  user_id: string;
  title: string;
  file_type?: string | null;
  word_count?: number | null;
  keywords?: string | null;
  created_at: string;
}

export interface ResumeAnalysisDetail {
  id: string;
  resume_id: string;
  title: string;
  created_at: string;
  readiness_score: number;
  ats_score: number;
  clarity_score: number;
  impact_score: number;
  skill_alignment_score: number;
  summary: string;
  detected_skills: string[];
  matching_skills: string[];
  missing_skills: string[];
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  target_role: string;
  target_company: string;
  word_count: number;
  // Category breakdown
  overall_score: number;
  keyword_match_score: number;
  skills_score: number;
  experience_score: number;
  project_score: number;
  education_score: number;
  formatting_score: number;

  // Extracted fields
  extracted_name?: string;
  extracted_email?: string;
  extracted_phone?: string;
  extracted_education: string[];
  extracted_experience: string[];
  extracted_projects: string[];
  extracted_technical_skills: string[];
  extracted_soft_skills: string[];
  extracted_certifications: string[];
  extracted_achievements: string[];
  extracted_links: string[];

  // Improvements
  missing_keywords: string[];
  formatting_issues: string[];
  content_improvements: string[];
  project_improvements: string[];
  experience_improvements: string[];

  before_after_suggestions: {
    original_text: string;
    improved_text: string;
    reason: string;
  }[];

  job_role_recommendations: {
    role: string;
    match_percentage: number;
    matching_skills: string[];
    missing_skills: string[];
    reason: string;
  }[];

  roles_requiring_preparation?: {
    role: string;
    match_percentage: number;
    matching_skills: string[];
    missing_skills: string[];
    reason: string;
  }[];

  role_suitability_explanation: string;
  role_suitability_score?: number;
  role_suitability_status?: string;
  ai_personalization_used: boolean;
  gemini_used?: boolean;
  fallback_used?: boolean;
}

export interface ResumeSummaryItem {
  id: string;
  resume_id: string;
  title: string;
  readiness_score: number;
  ats_score: number;
  created_at: string;
}
