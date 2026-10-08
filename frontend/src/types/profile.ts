export interface StudentProfile {
  id: string;
  user_id: string;
  headline: string | null;
  biography: string | null;
  target_company_id: string | null;
  target_role: string | null;
  target_company: string | null;
  current_level: string | null;
  interview_difficulty: string | null;
  career_goal: string | null;
  created_at: string;
  updated_at: string;
}
