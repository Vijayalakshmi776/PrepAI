export interface RoadmapTaskItem {
  id: string;
  title: string;
  description?: string | null;
  completed: boolean;
  priority: number;
  due_date?: string | null;
}

export interface SkillGapItem {
  id: string;
  skill_name: string;
  gap_description?: string | null;
  priority: number;
}

export interface ProgressMetrics {
  completed_count: number;
  total_tasks: number;
  completion_percentage: number;
  xp_points: number;
  streak_days: number;
}

export interface RoadmapDetail {
  roadmap_id: string;
  title: string;
  summary?: string | null;
  target_company: string;
  target_role: string;
  current_phase: string;
  company_recommendations: string[];
  tasks: RoadmapTaskItem[];
  skill_gaps: SkillGapItem[];
  progress: ProgressMetrics;
}

export interface TaskToggleResult {
  task_id: string;
  title: string;
  completed: boolean;
  progress: ProgressMetrics;
}
