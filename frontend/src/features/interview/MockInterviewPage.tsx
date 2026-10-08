import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Button } from '../../components/ui/Button';
import { ProgressRing } from '../../components/ProgressRing';
import { interviewApi, onboardingApi } from '../../services/api';
import type {
  CompanyInfo,
  InterviewFeedbackInfo,
  InterviewQuestionInfo,
  InterviewSessionDetail,
  InterviewSessionSummary,
} from '../../types/interview';

function getRoundCategory(title: string | undefined): 'Aptitude' | 'HR' | 'Coding' | 'Technical' {
  if (!title) return 'Technical';
  const t = title.toLowerCase();
  if (t.includes('aptitude') || t.includes('reasoning') || t.includes('quantitative') || t.includes('numerical')) return 'Aptitude';
  if (t.includes('hr') || t.includes('behavioral') || t.includes('managerial') || t.includes('culture') || t.includes('leadership') || t.includes('fit') || t.includes('founder')) return 'HR';
  if (t.includes('coding') || t.includes('algorithm') || t.includes('programming') || t.includes('dsa')) return 'Coding';
  return 'Technical';
}

const difficultyOptions = ['Easy', 'Medium', 'Hard'];
const roleOptions = [
  'Software Engineer',
  'Frontend Developer',
  'Backend Developer',
  'Full Stack Developer',
  'Data Analyst',
  'AI/ML Engineer',
];

type ViewMode = 'setup' | 'interview' | 'summary';

export function MockInterviewPage() {
  // State for setup
  const [companies, setCompanies] = useState<CompanyInfo[]>([]);
  const [loadingCompanies, setLoadingCompanies] = useState(true);
  const [selectedCompanyName, setSelectedCompanyName] = useState('TCS');
  const [selectedRole, setSelectedRole] = useState('Software Engineer');
  const [selectedDifficulty, setSelectedDifficulty] = useState('Medium');
  const [selectedRoundId, setSelectedRoundId] = useState<string>('');
  const [pastSessions, setPastSessions] = useState<InterviewSessionSummary[]>([]);

  // State for active interview session
  const [viewMode, setViewMode] = useState<ViewMode>('setup');
  const [currentSession, setCurrentSession] = useState<InterviewSessionDetail | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answerText, setAnswerText] = useState('');
  const [isStarting, setIsStarting] = useState(false);
  const [isSubmittingAnswer, setIsSubmittingAnswer] = useState(false);
  const [isCompleting, setIsCompleting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Question evaluations tracking
  const [evaluatedAnswers, setEvaluatedAnswers] = useState<
    Record<string, { score: number; feedback: string; response: string }>
  >({});
  const [summaryFeedback, setSummaryFeedback] = useState<InterviewFeedbackInfo | null>(null);

  // Load companies, past sessions, and restore active session on mount
  useEffect(() => {
    let cancelled = false;

    async function initData() {
      try {
        setLoadingCompanies(true);
        const [compList, sessionsList, profile] = await Promise.all([
          interviewApi.getCompanies(),
          interviewApi.listSessions().catch(() => []),
          onboardingApi.getMyProfile().catch(() => null),
        ]);

        if (!cancelled) {
          setCompanies(compList);
          setPastSessions(sessionsList);

          // Set default user profile choices BEFORE rendering setup controls to prevent async reset glitches
          if (profile) {
            if (profile.target_company) {
              const match = compList.find(
                (c) => c.name.toLowerCase() === profile.target_company?.toLowerCase()
              );
              if (match) setSelectedCompanyName(match.name);
            }
            if (profile.target_role) setSelectedRole(profile.target_role);
            if (profile.interview_difficulty) setSelectedDifficulty(profile.interview_difficulty);
          }

          // Restore active session after page refresh ONLY if explicitly present in localStorage
          const activeSessionId = localStorage.getItem('prepai_active_session_id');

          if (activeSessionId) {
            try {
              const session = await interviewApi.getSession(activeSessionId);
              if (!cancelled && session) {
                setCurrentSession(session);

                const restoredEvaluated: Record<string, { score: number; feedback: string; response: string }> = {};
                let firstUnansweredIdx = -1;
                session.questions.forEach((q, idx) => {
                  if (q.answer) {
                    restoredEvaluated[q.id] = {
                      score: q.answer.score ?? 0,
                      feedback: q.answer.score === 100 ? 'Correct answer!' : 'Submitted response.',
                      response: q.answer.response,
                    };
                  } else if (firstUnansweredIdx === -1) {
                    firstUnansweredIdx = idx;
                  }
                });
                setEvaluatedAnswers(restoredEvaluated);

                const targetIdx = firstUnansweredIdx !== -1 ? firstUnansweredIdx : 0;
                setCurrentQuestionIndex(targetIdx);
                const qTarget = session.questions[targetIdx];
                setAnswerText(restoredEvaluated[qTarget?.id]?.response || '');

                if (session.completed) {
                  if (session.feedback) setSummaryFeedback(session.feedback);
                  setViewMode('summary');
                } else {
                  setViewMode('interview');
                }
              }
            } catch {
              localStorage.removeItem('prepai_active_session_id');
            }
          }
        }
      } catch (err) {
        if (!cancelled) {
          setErrorMessage(err instanceof Error ? err.message : 'Failed to load company patterns.');
        }
      } finally {
        if (!cancelled) setLoadingCompanies(false);
      }
    }

    void initData();
    return () => {
      cancelled = true;
    };
  }, []);

  // Compute selected company object & available rounds
  const selectedCompany = companies.find(
    (c) => c.name.toLowerCase() === selectedCompanyName.toLowerCase()
  ) || companies[0];

  const availableRounds = selectedCompany?.patterns?.[0]?.rounds || [];

  // Update selected round when company or companies catalog changes
  useEffect(() => {
    const rounds = selectedCompany?.patterns?.[0]?.rounds || [];
    if (rounds.length > 0) {
      setSelectedRoundId(rounds[0].id);
    }
  }, [selectedCompanyName, companies]);

  const selectedRound = availableRounds.find((r) => r.id === selectedRoundId);

  // Start interview handler
  const handleStartInterview = async () => {
    setIsStarting(true);
    setErrorMessage(null);
    try {
      const session = await interviewApi.startSession({
        company_name: selectedCompanyName,
        role: selectedRole,
        difficulty: selectedDifficulty,
        round_title: selectedRound?.title || 'Technical Round',
        round_id: selectedRound?.id,
        company_id: selectedCompany?.id,
      });

      localStorage.setItem('prepai_active_session_id', session.id);
      setCurrentSession(session);
      setCurrentQuestionIndex(0);
      setAnswerText('');
      setEvaluatedAnswers({});
      setSummaryFeedback(null);
      setViewMode('interview');
    } catch (err) {
      setErrorMessage(err instanceof Error ? err.message : 'Failed to start interview session.');
    } finally {
      setIsStarting(false);
    }
  };

  // Current question helper
  const questions: InterviewQuestionInfo[] = currentSession?.questions || [];
  const currentQuestion: InterviewQuestionInfo | undefined = questions[currentQuestionIndex];
  const currentEvaluation = currentQuestion ? evaluatedAnswers[currentQuestion.id] : undefined;

  const currentRoundTitle = currentSession?.current_round?.title;
  const roundCategory = getRoundCategory(currentRoundTitle);

  // Check if current question has an answer provided (either saved in state or entered in input)
  const isCurrentAnswered = Boolean(
    (currentQuestion && evaluatedAnswers[currentQuestion.id]?.response) ||
    answerText.trim()
  );

  // Submit single answer
  const handleSubmitAnswer = async (overrideText?: string, silent: boolean = false) => {
    const textToSubmit = overrideText ?? answerText;
    if (!currentQuestion || !textToSubmit.trim()) return;

    if (!silent) setIsSubmittingAnswer(true);
    if (!silent) setErrorMessage(null);
    try {
      const result = await interviewApi.submitAnswer(currentQuestion.id, {
        response: textToSubmit.trim(),
      });

      setEvaluatedAnswers((prev) => ({
        ...prev,
        [currentQuestion.id]: {
          score: result.score,
          feedback: result.feedback,
          response: result.response,
        },
      }));
    } catch (err) {
      if (!silent) setErrorMessage(err instanceof Error ? err.message : 'Failed to submit answer.');
      throw err;
    } finally {
      if (!silent) setIsSubmittingAnswer(false);
    }
  };

  // Next question / Finish
  const handleNext = async () => {
    if (currentQuestion && answerText.trim() && !evaluatedAnswers[currentQuestion.id]) {
      try {
        await handleSubmitAnswer(answerText.trim(), false);
      } catch (err) {
        setErrorMessage(err instanceof Error ? err.message : 'Failed to evaluate final answer.');
        return;
      }
    }

    if (currentQuestionIndex < questions.length - 1) {
      const nextIdx = currentQuestionIndex + 1;
      setCurrentQuestionIndex(nextIdx);
      const nextQ = questions[nextIdx];
      setAnswerText(evaluatedAnswers[nextQ.id]?.response || '');
    } else {
      await handleFinishSession();
    }
  };

  // Complete interview & generate summary
  const handleFinishSession = async () => {
    if (!currentSession) return;
    setIsCompleting(true);
    setErrorMessage(null);
    try {
      const feedback = await interviewApi.completeSession(currentSession.id);
      // Retain prepai_active_session_id in localStorage so refreshing the summary page reloads the session summary cleanly
      setSummaryFeedback(feedback);
      setViewMode('summary');

      // Refresh past sessions
      interviewApi.listSessions().then(setPastSessions).catch(() => {});
    } catch (err) {
      setErrorMessage(err instanceof Error ? err.message : 'Failed to complete interview session.');
    } finally {
      setIsCompleting(false);
    }
  };

  // Reset to setup
  const handleReset = () => {
    localStorage.removeItem('prepai_active_session_id');
    setViewMode('setup');
    setCurrentSession(null);
    setEvaluatedAnswers({});
    setSummaryFeedback(null);
    setAnswerText('');
    setErrorMessage(null);
  };

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <section className="space-y-3 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">
              AI Mock Interview Practice
            </p>
            <h1 className="mt-1 text-3xl font-bold text-slate-950">
              {viewMode === 'setup' && 'Prepare with real company interview patterns'}
              {viewMode === 'interview' && `Live Session: ${currentSession?.title || 'Mock Interview'}`}
              {viewMode === 'summary' && 'Interview Performance & AI Evaluation Summary'}
            </h1>
          </div>
          {viewMode !== 'setup' && (
            <Button variant="ghost" onClick={handleReset} className="border border-slate-200">
              New Interview
            </Button>
          )}
        </div>
        <p className="max-w-3xl text-sm leading-7 text-slate-600">
          {viewMode === 'setup' &&
            'Select your target company and interview round to practice adaptive, technical, and behavioral questions with instant AI feedback.'}
          {viewMode === 'interview' &&
            'Answer each prompt with structure and technical clarity. Your responses and scores are evaluated and persisted in real time.'}
          {viewMode === 'summary' &&
            'Review your overall readiness score, AI performance critique, strengths, and targeted improvement recommendations.'}
        </p>
      </section>

      {/* Error Alert */}
      {errorMessage && (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm font-medium text-rose-700">
          {errorMessage}
        </div>
      )}

      {/* VIEW 1: SETUP & CONFIGURATION */}
      {viewMode === 'setup' && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Company Selection */}
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-slate-900">Target Company</span>
                {selectedCompany?.company_type && (
                  <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
                    {selectedCompany.company_type}
                  </span>
                )}
              </div>
              <p className="mt-1 text-xs text-slate-500">PrepAI practice simulations based on publicly known interview formats (not actual confidential company questions).</p>

              {loadingCompanies ? (
                <div className="mt-4 py-3 text-sm text-slate-500">Loading company catalog…</div>
              ) : (
                <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-2">
                  {companies.map((c) => {
                    const isSelected = c.name.toLowerCase() === selectedCompanyName.toLowerCase();
                    return (
                      <button
                        key={c.name}
                        type="button"
                        onClick={() => setSelectedCompanyName(c.name)}
                        className={`rounded-2xl border p-3 text-left transition ${
                          isSelected
                            ? 'border-primary bg-primary/10 text-primary font-semibold shadow-sm'
                            : 'border-slate-200 bg-white text-slate-700 hover:border-primary/50'
                        }`}
                      >
                        <span className="block text-sm font-bold">{c.name}</span>
                        <span className="mt-1 block text-xs text-slate-500">{c.difficulty_level || 'Medium'}</span>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Target Role Selection */}
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
              <span className="text-sm font-semibold text-slate-900">Target Engineering Role</span>
              <p className="mt-1 text-xs text-slate-500">Customizes question domain and depth</p>
              <div className="mt-4 space-y-2">
                {roleOptions.map((r) => {
                  const isSelected = r === selectedRole;
                  return (
                    <button
                      key={r}
                      type="button"
                      onClick={() => setSelectedRole(r)}
                      className={`w-full rounded-2xl border px-4 py-2.5 text-left text-sm transition ${
                        isSelected
                          ? 'border-primary bg-primary/10 text-primary font-semibold'
                          : 'border-slate-200 bg-white text-slate-700 hover:border-primary/50'
                      }`}
                    >
                      {r}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Difficulty */}
            <div className="space-y-6 rounded-3xl border border-slate-200 bg-slate-50 p-6">
              <div>
                <span className="text-sm font-semibold text-slate-900">Difficulty</span>
                <div className="mt-2 flex gap-2">
                  {difficultyOptions.map((diff) => (
                    <button
                      key={diff}
                      type="button"
                      onClick={() => setSelectedDifficulty(diff)}
                      className={`flex-1 rounded-xl border py-2 text-center text-xs font-semibold transition ${
                        selectedDifficulty === diff
                          ? 'border-primary bg-primary text-white shadow-sm'
                          : 'border-slate-200 bg-white text-slate-700 hover:border-primary/50'
                      }`}
                    >
                      {diff}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Action Row */}
          <div className="flex flex-col items-center justify-between gap-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:flex-row">
            <div>
              <p className="text-base font-semibold text-slate-950">
                Ready to practice for <span className="text-primary">{selectedCompanyName}</span>?
              </p>
              <p className="text-xs text-slate-500">
                {selectedRole} • Full Interview Loop • {selectedDifficulty} Difficulty
              </p>
            </div>
            <Button
              onClick={handleStartInterview}
              disabled={isStarting}
              className="min-w-[200px]"
            >
              {isStarting ? 'Setting up session…' : 'Start Mock Interview'}
            </Button>
          </div>

          {/* Past Sessions History */}
          {pastSessions.length > 0 && (
            <div className="space-y-4 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
              <h2 className="text-xl font-bold text-slate-950">Your Past Mock Interviews</h2>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {pastSessions.map((s) => (
                  <div
                    key={s.id}
                    className="rounded-3xl border border-slate-200 bg-slate-50 p-5 transition hover:shadow-md"
                  >
                    <div className="flex items-center justify-between">
                      <span
                        className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                          s.completed ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
                        }`}
                      >
                        {s.completed ? 'Completed' : 'In Progress'}
                      </span>
                      <span className="text-xs text-slate-400">
                        {new Date(s.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <h3 className="mt-3 text-sm font-bold text-slate-900 line-clamp-1">{s.title}</h3>
                    <p className="mt-1 text-xs text-slate-500">
                      {s.answers_count} of {s.questions_count} questions answered
                    </p>
                    {s.feedback?.summary && (
                      <p className="mt-2 text-xs italic text-slate-600 line-clamp-2">
                        "{s.feedback.summary}"
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      )}

      {/* VIEW 2: ACTIVE INTERVIEW */}
      {viewMode === 'interview' && currentQuestion && (
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
          {/* Question Stepper & Meta */}
          <div className="flex flex-col gap-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary text-sm font-bold text-white shadow-soft">
                {currentSession?.current_round?.round_number || 1}
              </span>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Round {currentSession?.current_round?.round_number || 1} of {currentSession?.current_round?.total_rounds || 1} • {roundCategory.toUpperCase()}
                </p>
                <p className="text-sm font-bold text-slate-900">
                  {currentSession?.current_round?.title || 'Mock Interview Round'}
                </p>
                <p className="mt-0.5 text-xs text-slate-500">
                  Question {currentQuestionIndex + 1} of {questions.length}
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              {questions.map((q, idx) => {
                const isAnswered = Boolean(evaluatedAnswers[q.id]);
                const isCurrent = idx === currentQuestionIndex;
                return (
                  <button
                    key={q.id}
                    type="button"
                    onClick={() => {
                      setCurrentQuestionIndex(idx);
                      setAnswerText(evaluatedAnswers[q.id]?.response || '');
                    }}
                    className={`h-9 w-9 rounded-xl text-xs font-bold transition ${
                      isCurrent
                        ? 'bg-primary text-white shadow-soft ring-2 ring-primary/20'
                        : isAnswered
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'border border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100'
                    }`}
                  >
                    {idx + 1}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Question Prompt Card */}
          <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-8">
            <div className="flex items-center justify-between">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">
                Interviewer Prompt
              </p>
              <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-bold text-primary">
                Question {currentQuestionIndex + 1} of {questions.length}
              </span>
            </div>
            <h2 className="mt-3 text-2xl font-bold leading-snug text-slate-950">
              {currentQuestion.prompt}
            </h2>
          </div>

          {/* Student Answer Input Box */}
          <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
            <div className="mb-4 flex items-center justify-between">
              <label htmlFor="answer-input" className="text-sm font-semibold text-slate-900">
                {roundCategory === 'Coding' ? 'Your Answer & Technical Explanation' : 'Your Answer'}
              </label>
              <span className="text-xs text-slate-400">
                {answerText.trim().split(/\s+/).filter(Boolean).length} words
              </span>
            </div>

            {['mcq', 'aptitude'].includes(currentQuestion.question_type?.toLowerCase() || '') && currentQuestion.options && currentQuestion.options.length > 0 ? (
              <div className="mt-2 flex flex-col gap-3">
                {currentQuestion.options.map((opt, i) => (
                  <label
                    key={i}
                    className={`flex cursor-pointer items-center gap-4 rounded-xl border p-4 transition ${
                      answerText === opt
                        ? 'border-primary bg-primary/5 font-semibold text-primary'
                        : 'border-slate-200 bg-slate-50 text-slate-700 hover:border-slate-300 hover:bg-slate-100'
                    }`}
                  >
                    <input
                      type="radio"
                      name={`q-${currentQuestion.id}`}
                      value={opt}
                      onChange={(e) => {
                        const val = e.target.value;
                        setAnswerText(val);
                        void handleSubmitAnswer(val, true);
                      }}
                      checked={answerText === opt}
                      className="peer hidden"
                    />
                    <span className="flex h-5 w-5 items-center justify-center rounded-full border border-current">
                      {answerText === opt && <span className="h-2.5 w-2.5 rounded-full bg-current"></span>}
                    </span>
                    <span>{opt}</span>
                  </label>
                ))}
              </div>
            ) : (
              <textarea
                id="answer-input"
                rows={7}
                value={answerText}
                onChange={(e) => setAnswerText(e.target.value)}
                placeholder={
                  roundCategory === 'Coding'
                    ? 'State your approach clearly. Detail the algorithm/data structure, time and space complexity, trade-offs, and edge case handling...'
                    : roundCategory === 'HR'
                    ? 'Structure your response using the STAR method (Situation, Task, Action, Result). Detail your specific impact and learnings...'
                    : 'Provide a detailed technical explanation, mentioning specific patterns, architecture, or tools...'
                }
                className="w-full rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm text-slate-900 outline-none transition focus:border-primary focus:bg-white focus:ring-2 focus:ring-primary/10"
              />
            )}

            <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <p className="text-xs text-slate-500">
                💡 Tip: {
                  roundCategory === 'Coding'
                    ? 'Structure your response with intuition, step-by-step logic, and complexity analysis.'
                    : roundCategory === 'Aptitude'
                    ? 'Select the correct option. Your answer is automatically saved.'
                    : roundCategory === 'HR'
                    ? 'Focus on real experiences and highlight your specific contributions and outcomes.'
                    : 'Be clear and mention relevant technical trade-offs and design patterns.'
                }
              </p>
              {roundCategory !== 'Aptitude' && (
                <Button
                  onClick={() => handleSubmitAnswer()}
                  disabled={isSubmittingAnswer || !answerText.trim()}
                  className="min-w-[180px]"
                >
                  {isSubmittingAnswer ? 'Evaluating…' : currentEvaluation ? 'Update Answer' : 'Submit for Evaluation'}
                </Button>
              )}
            </div>
          </div>

          {/* Live AI Feedback on Current Question */}
          <AnimatePresence>
            {currentEvaluation && roundCategory !== 'Aptitude' && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="rounded-[2rem] border border-emerald-200 bg-emerald-50/70 p-6 shadow-sm"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-600 text-sm font-bold text-white">
                      ✓
                    </span>
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-wider text-emerald-800">
                        AI Real-Time Evaluation
                      </p>
                      <p className="text-sm font-bold text-emerald-950">
                        Score: {currentEvaluation.score} / 100
                      </p>
                    </div>
                  </div>
                  <span className="rounded-full bg-emerald-200/80 px-3 py-1 text-xs font-bold text-emerald-900">
                    Saved to PostgreSQL
                  </span>
                </div>
                <p className="mt-4 text-sm leading-6 text-emerald-900">
                  {currentEvaluation.feedback}
                </p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Navigation Controls */}
          <div className="flex items-center justify-between gap-4">
            <Button
              variant="ghost"
              disabled={currentQuestionIndex === 0}
              onClick={() => {
                const prevIdx = currentQuestionIndex - 1;
                setCurrentQuestionIndex(prevIdx);
                setAnswerText(evaluatedAnswers[questions[prevIdx].id]?.response || '');
              }}
              className="border border-slate-200"
            >
              Previous Question
            </Button>

            <Button
              onClick={handleNext}
              disabled={isCompleting || isSubmittingAnswer || (currentQuestionIndex === questions.length - 1 && !isCurrentAnswered)}
              className="min-w-[200px]"
            >
              {isCompleting
                ? 'Generating Summary…'
                : currentQuestionIndex === questions.length - 1
                ? 'Finish & View AI Summary'
                : 'Next Question →'}
            </Button>
          </div>
        </motion.div>
      )}

      {/* VIEW 3: INTERVIEW SUMMARY & EVALUATION REPORT */}
      {viewMode === 'summary' && summaryFeedback && (
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
          {/* Executive Score Card */}
          <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
            <div className="grid gap-8 lg:grid-cols-[0.8fr_1.2fr] lg:items-center">
              <div className="flex flex-col items-center justify-center rounded-3xl border border-slate-100 bg-slate-50 p-6 text-center">
                <ProgressRing
                  progress={summaryFeedback.overall_score || 75}
                  label="Interview Readiness"
                />
                <p className="mt-4 text-xs font-semibold uppercase tracking-wider text-slate-500">
                  {selectedCompanyName} • {selectedRole}
                </p>
                <p className="mt-1 text-xs text-slate-400">
                  Round: {selectedRound?.title || 'Technical'}
                </p>
              </div>

              <div className="space-y-4">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">
                  Executive AI Critique
                </p>
                <h2 className="text-2xl font-bold text-slate-950">
                  Performance Breakdown & Company Fit
                </h2>
                <p className="text-sm leading-7 text-slate-700">
                  {summaryFeedback.summary}
                </p>
              </div>
            </div>
          </div>

          {/* Detailed Strengths & Recommendations Grid */}
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Strengths */}
            <div className="rounded-3xl border border-emerald-200 bg-emerald-50/50 p-6">
              <div className="flex items-center gap-2 text-emerald-800">
                <span className="text-lg">💪</span>
                <h3 className="text-base font-bold">Key Strengths</h3>
              </div>
              <div className="mt-4 whitespace-pre-line text-sm leading-6 text-emerald-900">
                {summaryFeedback.strengths}
              </div>
            </div>

            {/* Areas for Improvement */}
            <div className="rounded-3xl border border-amber-200 bg-amber-50/50 p-6">
              <div className="flex items-center gap-2 text-amber-800">
                <span className="text-lg">🎯</span>
                <h3 className="text-base font-bold">Areas for Improvement</h3>
              </div>
              <div className="mt-4 whitespace-pre-line text-sm leading-6 text-amber-900">
                {summaryFeedback.weaknesses}
              </div>
            </div>

            {/* Recommendations */}
            <div className="rounded-3xl border border-primary/20 bg-primary/5 p-6">
              <div className="flex items-center gap-2 text-primary">
                <span className="text-lg">🚀</span>
                <h3 className="text-base font-bold">Targeted Next Steps</h3>
              </div>
              <div className="mt-4 whitespace-pre-line text-sm leading-6 text-slate-800">
                {summaryFeedback.recommendations}
              </div>
            </div>
          </div>

          {/* Question-by-Question Log */}
          {questions.length > 0 && (
            <div className="space-y-4 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
              <h3 className="text-xl font-bold text-slate-950">Question Review Log</h3>
              <div className="space-y-4">
                {questions.map((q, idx) => {
                  const evalData = evaluatedAnswers[q.id];
                  return (
                    <div
                      key={q.id}
                      className="rounded-2xl border border-slate-200 bg-slate-50 p-5 space-y-3"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                          Question {idx + 1}
                        </span>
                        {evalData && (
                          <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-bold text-primary">
                            Score: {evalData.score} / 100
                          </span>
                        )}
                      </div>
                      <p className="text-sm font-semibold text-slate-900">{q.prompt}</p>
                      {evalData ? (
                        <div className="rounded-xl border border-slate-200 bg-white p-4 text-xs leading-relaxed text-slate-700">
                          <p className="font-semibold text-slate-500">Your Answer:</p>
                          <p className={`mt-1 text-sm ${q.question_type === 'mcq' ? (evalData.score === 100 ? 'font-bold text-emerald-600' : 'font-bold text-rose-600') : ''}`}>
                            {q.question_type === 'mcq' ? (evalData.score === 100 ? '✓ ' : '✗ ') : ''}{evalData.response}
                          </p>
                          <p className="mt-3 font-semibold text-primary">
                            {q.question_type === 'mcq' && evalData.score === 0 ? 'Correct Answer & Feedback:' : 'AI Feedback:'}
                          </p>
                          <p className="mt-1 text-slate-600">{evalData.feedback}</p>
                        </div>
                      ) : (
                        <p className="text-xs italic text-slate-400">No answer submitted.</p>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Action Row */}
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <Button onClick={handleReset} className="min-w-[200px]">
              Practice Another Round
            </Button>
            <Button as={Link} to="/dashboard" variant="ghost" className="border border-slate-200">
              Return to Dashboard
            </Button>
          </div>
        </motion.div>
      )}
    </div>
  );
}
