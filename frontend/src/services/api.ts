import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios';
import type { UserProfile } from '../types/auth';
import type { StudentProfile } from '../types/profile';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8010';

const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

function getStoredToken(): string | null {
  return window.localStorage.getItem('prepai_access_token');
}

apiClient.interceptors.request.use((config) => {
  const token = getStoredToken();
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type'];
    delete config.headers['content-type'];
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      window.localStorage.removeItem('prepai_access_token');
    }
    return Promise.reject(error);
  },
);

function buildErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    if (import.meta.env.DEV) {
      console.error('[PrepAI API Error Log]', {
        url: error.config?.url,
        method: error.config?.method,
        status: error.response?.status,
        data: error.response?.data,
        code: error.code,
        message: error.message,
      });
    }
    const data = error.response?.data;
    if (typeof data === 'object' && data && 'detail' in data) {
      const detail = (data as Record<string, unknown>).detail;
      if (typeof detail === 'string') {
        return detail;
      }
      if (Array.isArray(detail)) {
        return detail.map((item: Record<string, unknown>) => item.msg || (Array.isArray(item.loc) ? item.loc.join('.') : '')).join(', ');
      }
    }
    if (error.response?.status === 401) return 'Your session has expired. Please log in again.';
    if (error.response?.status === 403) return 'You do not have permission to perform this action.';
    if (error.response?.status === 404) return 'The requested resource was not found.';
    if (error.response?.status === 409) return 'An account with this email already exists.';
    if (error.response?.status === 422) return 'Invalid form input or parameter format. Please check your submission.';
    if (error.response?.status && error.response.status >= 500) return 'The server encountered an error processing your request. Please try again shortly.';
    if (error.code === 'ERR_NETWORK' || !error.response) return `Unable to reach the backend at ${API_BASE_URL}. The server may be starting up — please try again in a few seconds.`;
  }
  return 'Something went wrong. Please try again.';
}

export async function request<T>(config: AxiosRequestConfig): Promise<T> {
  try {
    const response = await apiClient.request<T>(config);
    return response.data;
  } catch (error) {
    throw new Error(buildErrorMessage(error));
  }
}

export const authApi = {
  register: (payload: { email: string; full_name?: string; password: string }) =>
    request<UserProfile>({ method: 'POST', url: '/auth/register', data: payload }),

  login: (payload: { email: string; password: string }) =>
    request<{ access_token: string; token_type: string }>({
      method: 'POST',
      url: '/auth/token',
      data: payload,
    }),

  me: () => request<UserProfile>({ method: 'GET', url: '/auth/me' }),
};

export const onboardingApi = {
  submit: (payload: {
    user_type: string;
    career_goal: string;
    company_type: string;
    dream_company: string;
    target_role: string;
    current_level: string;
    interview_difficulty?: string;
    skills: string[];
  }) =>
    request<{ status: string; message: string; profile_id?: string }>({
      method: 'POST',
      url: '/onboarding/',
      data: payload,
    }),

  getMyProfile: () =>
    request<StudentProfile>({ method: 'GET', url: '/onboarding/me' }),
};

import type { CompanyInfo, InterviewFeedbackInfo, InterviewSessionDetail, InterviewSessionSummary } from '../types/interview';
import type { RoadmapDetail, TaskToggleResult, SkillGapItem, ProgressMetrics } from '../types/roadmap';

export const interviewApi = {
  getCompanies: () =>
    request<CompanyInfo[]>({ method: 'GET', url: '/interview/companies' }),

  startSession: (payload: {
    company_name: string;
    role: string;
    difficulty: string;
    round_title?: string;
    round_id?: string;
    company_id?: string;
  }) =>
    request<InterviewSessionDetail>({
      method: 'POST',
      url: '/interview/sessions',
      data: payload,
    }),

  listSessions: () =>
    request<InterviewSessionSummary[]>({ method: 'GET', url: '/interview/sessions' }),

  getSession: (sessionId: string) =>
    request<InterviewSessionDetail>({ method: 'GET', url: `/interview/sessions/${sessionId}` }),

  submitAnswer: (questionId: string, payload: { response: string }) =>
    request<{
      answer_id: string;
      question_id: string;
      score: number;
      feedback: string;
      response: string;
    }>({
      method: 'POST',
      url: `/interview/questions/${questionId}/answer`,
      data: payload,
    }),

  completeSession: (sessionId: string) =>
    request<InterviewFeedbackInfo>({
      method: 'POST',
      url: `/interview/sessions/${sessionId}/complete`,
    }),
};

export const roadmapApi = {
  getMyRoadmap: () =>
    request<RoadmapDetail>({ method: 'GET', url: '/roadmap/me' }),

  regenerateRoadmap: () =>
    request<RoadmapDetail>({ method: 'POST', url: '/roadmap/generate' }),

  toggleTask: (taskId: string) =>
    request<TaskToggleResult>({
      method: 'PATCH',
      url: `/roadmap/tasks/${taskId}/toggle`,
    }),

  getSkillGaps: () =>
    request<SkillGapItem[]>({ method: 'GET', url: '/roadmap/skill-gaps' }),

  getProgress: () =>
    request<ProgressMetrics>({ method: 'GET', url: '/roadmap/progress' }),
};

import type { ResumeAnalysisDetail, ResumeSummaryItem } from '../types/resume';


export const resumeApi = {
  analyzeResume: (file: File, targetRole?: string) => {
    const formData = new FormData();
    formData.append('file', file);
    if (targetRole) {
      formData.append('target_role', targetRole);
    }
    return request<ResumeAnalysisDetail>({
      method: 'POST',
      url: '/resume/analyze',
      data: formData,
    });
  },

  getLatestAnalysis: () =>
    request<ResumeAnalysisDetail>({ method: 'GET', url: '/resume/latest' }),

  getHistory: () =>
    request<ResumeSummaryItem[]>({ method: 'GET', url: '/resume/history' }),

  getAnalysis: (resumeId: string) =>
    request<ResumeAnalysisDetail>({ method: 'GET', url: `/resume/${resumeId}` }),

  deleteResume: (resumeId: string) =>
    request<{ status: string; message: string }>({
      method: 'DELETE',
      url: `/resume/${resumeId}`,
    }),
};

export { API_BASE_URL };


