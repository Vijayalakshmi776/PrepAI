import { useEffect, useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle2,
  Circle,
  RefreshCw,
  Target,
  Flame,
  Award,
  Sparkles,
  BookOpen,
  Briefcase,
  AlertTriangle,
  Clock,
  ArrowRight,
  Filter,
  Check,
  ChevronDown,
  ChevronUp,
  Layers,
  Info,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { roadmapApi } from '../../services/api';
import type { RoadmapDetail, RoadmapTaskItem } from '../../types/roadmap';

type FilterType = 'all' | 'pending' | 'completed';

export function RoadmapPage() {
  const [roadmap, setRoadmap] = useState<RoadmapDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<FilterType>('all');
  const [togglingTaskId, setTogglingTaskId] = useState<string | null>(null);
  const [expandedTaskIds, setExpandedTaskIds] = useState<Set<string>>(new Set());

  const fetchRoadmap = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await roadmapApi.getMyRoadmap();
      setRoadmap(data);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to load roadmap';
      setError(msg);
      setRoadmap(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap();
  }, []);

  const handleRegenerate = async () => {
    try {
      setRegenerating(true);
      setError(null);
      const data = await roadmapApi.regenerateRoadmap();
      setRoadmap(data);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to regenerate roadmap';
      setError(msg);
    } finally {
      setRegenerating(false);
    }
  };

  const handleToggleTask = async (task: RoadmapTaskItem) => {
    if (!roadmap || togglingTaskId) return;

    const previousRoadmap = { ...roadmap };
    const newCompleted = !task.completed;

    // Optimistic UI update
    const updatedTasks = roadmap.tasks.map((t) =>
      t.id === task.id ? { ...t, completed: newCompleted } : t
    );
    const completedCount = updatedTasks.filter((t) => t.completed).length;
    const totalTasks = updatedTasks.length;
    const completionPercentage = totalTasks > 0 ? Math.round((completedCount / totalTasks) * 100) : 0;
    const xpPoints = completedCount * 50;

    setRoadmap({
      ...roadmap,
      tasks: updatedTasks,
      progress: {
        ...roadmap.progress,
        completed_count: completedCount,
        completion_percentage: completionPercentage,
        xp_points: xpPoints,
      },
    });

    try {
      setTogglingTaskId(task.id);
      const res = await roadmapApi.toggleTask(task.id);
      // Sync with server's calculated progress
      setRoadmap((prev) => {
        if (!prev) return null;
        return {
          ...prev,
          tasks: prev.tasks.map((t) => (t.id === task.id ? { ...t, completed: res.completed } : t)),
          progress: res.progress,
        };
      });
    } catch (err: unknown) {
      // Rollback on failure
      setRoadmap(previousRoadmap);
      const msg = err instanceof Error ? err.message : 'Failed to update task status';
      setError(msg);
    } finally {
      setTogglingTaskId(null);
    }
  };

  const toggleTaskExpansion = (taskId: string) => {
    setExpandedTaskIds((prev) => {
      const next = new Set(prev);
      if (next.has(taskId)) {
        next.delete(taskId);
      } else {
        next.add(taskId);
      }
      return next;
    });
  };

  const filteredTasks = useMemo(() => {
    if (!roadmap) return [];
    if (filter === 'completed') return roadmap.tasks.filter((t) => t.completed);
    if (filter === 'pending') return roadmap.tasks.filter((t) => !t.completed);
    return roadmap.tasks;
  }, [roadmap, filter]);

  // Loading Skeleton State
  if (loading) {
    return (
      <div className="space-y-8 animate-pulse">
        <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
          <div className="h-4 w-32 rounded-full bg-slate-200" />
          <div className="mt-4 h-8 w-2/3 rounded-xl bg-slate-200" />
          <div className="mt-2 h-4 w-1/2 rounded-md bg-slate-100" />
          <div className="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-24 rounded-2xl bg-slate-100" />
            ))}
          </div>
        </div>
        <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="space-y-4">
            <div className="h-6 w-48 rounded-md bg-slate-200" />
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-20 rounded-2xl bg-slate-100" />
            ))}
          </div>
          <div className="space-y-6">
            <div className="h-48 rounded-2xl bg-slate-100" />
            <div className="h-48 rounded-2xl bg-slate-100" />
          </div>
        </div>
      </div>
    );
  }

  // Error or Not Found / Pre-Onboarding State
  if (error && !roadmap) {
    const isNotOnboarded = error.toLowerCase().includes('onboarding') || error.toLowerCase().includes('not found');
    return (
      <div className="mx-auto max-w-2xl rounded-[2rem] border border-slate-200 bg-white p-10 text-center shadow-soft">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10 text-primary">
          {isNotOnboarded ? <Compass className="h-8 w-8" /> : <AlertTriangle className="h-8 w-8 text-amber-500" />}
        </div>
        <h2 className="mt-6 text-2xl font-bold text-slate-950">
          {isNotOnboarded ? 'Complete Onboarding to Generate Your Roadmap' : 'Unable to Load Roadmap'}
        </h2>
        <p className="mt-3 text-slate-600">
          {isNotOnboarded
            ? 'We customize your placement curriculum based on your dream company, role, current level, and target goals.'
            : error}
        </p>
        <div className="mt-8 flex justify-center gap-4">
          {isNotOnboarded ? (
            <Button as={Link} to="/onboarding" className="inline-flex items-center gap-2">
              Start Onboarding <ArrowRight className="h-4 w-4" />
            </Button>
          ) : (
            <Button onClick={fetchRoadmap} className="inline-flex items-center gap-2">
              <RefreshCw className="h-4 w-4" /> Try Again
            </Button>
          )}
        </div>
      </div>
    );
  }

  if (!roadmap) return null;

  const { progress } = roadmap;

  return (
    <div className="space-y-8">
      {/* Top Banner & Overview Card */}
      <section className="relative overflow-hidden rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
          <div className="space-y-3">
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-1.5 rounded-full bg-primary/10 px-3.5 py-1 text-xs font-bold uppercase tracking-wider text-primary">
                <Target className="h-3.5 w-3.5" />
                {roadmap.target_company} Placement Track
              </span>
              <span className="inline-flex items-center gap-1.5 rounded-full bg-slate-100 px-3.5 py-1 text-xs font-semibold text-slate-700">
                <Briefcase className="h-3.5 w-3.5 text-slate-500" />
                {roadmap.target_role}
              </span>
            </div>

            <h1 className="text-2xl font-black text-slate-950 sm:text-3xl lg:text-4xl">
              {roadmap.title}
            </h1>

            {roadmap.summary && (
              <p className="max-w-3xl text-sm text-slate-600 sm:text-base">
                {roadmap.summary}
              </p>
            )}

            <div className="flex items-center gap-2 pt-1">
              <span className="inline-flex items-center gap-1.5 rounded-xl border border-indigo-200 bg-indigo-50/80 px-3 py-1 text-xs font-semibold text-indigo-700">
                <Layers className="h-3.5 w-3.5" /> Current: {roadmap.current_phase}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              onClick={handleRegenerate}
              disabled={regenerating}
              className="inline-flex items-center gap-2 border-slate-300 hover:bg-slate-50"
            >
              <RefreshCw className={`h-4 w-4 ${regenerating ? 'animate-spin text-primary' : 'text-slate-600'}`} />
              {regenerating ? 'Regenerating...' : 'Refresh Roadmap'}
            </Button>
            <Button as={Link} to="/interview" className="inline-flex items-center gap-2">
              <Sparkles className="h-4 w-4" /> Practice Interview
            </Button>
          </div>
        </div>

        {/* Progress & Metrics Strip */}
        <div className="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
          <div className="rounded-2xl border border-slate-100 bg-slate-50/80 p-4 transition hover:bg-slate-50">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Overall Progress</span>
              <TrendingIcon percentage={progress.completion_percentage} />
            </div>
            <p className="mt-2 text-2xl font-black text-slate-950 sm:text-3xl">{progress.completion_percentage}%</p>
            <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-200">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-primary to-indigo-600"
                initial={{ width: 0 }}
                animate={{ width: `${progress.completion_percentage}%` }}
                transition={{ duration: 0.6, ease: 'easeOut' }}
              />
            </div>
          </div>

          <div className="rounded-2xl border border-slate-100 bg-slate-50/80 p-4 transition hover:bg-slate-50">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Tasks Completed</span>
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="mt-2 text-2xl font-black text-slate-950 sm:text-3xl">
              {progress.completed_count} <span className="text-sm font-normal text-slate-500">/ {progress.total_tasks}</span>
            </p>
            <p className="mt-2 text-xs text-slate-500">
              {progress.total_tasks - progress.completed_count} remaining
            </p>
          </div>

          <div className="rounded-2xl border border-slate-100 bg-slate-50/80 p-4 transition hover:bg-slate-50">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">XP Points</span>
              <Award className="h-4 w-4 text-amber-500" />
            </div>
            <p className="mt-2 text-2xl font-black text-amber-600 sm:text-3xl">+{progress.xp_points}</p>
            <p className="mt-2 text-xs text-slate-500">+50 XP per completed task</p>
          </div>

          <div className="rounded-2xl border border-slate-100 bg-slate-50/80 p-4 transition hover:bg-slate-50">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Prep Streak</span>
              <Flame className="h-4 w-4 text-orange-500" />
            </div>
            <p className="mt-2 text-2xl font-black text-orange-600 sm:text-3xl">{progress.streak_days} Day</p>
            <p className="mt-2 text-xs text-slate-500">Keep up the daily momentum!</p>
          </div>
        </div>
      </section>

      {/* Main Content Layout: Tasks on left, Skill Gaps & Insights on right */}
      <div className="grid gap-8 lg:grid-cols-[1.3fr_0.9fr]">
        {/* Left Column: Learning Tasks */}
        <section className="space-y-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-950 sm:text-2xl">Personalized Learning Tasks</h2>
              <p className="text-sm text-slate-600">Complete tasks to master placement requirements step-by-step.</p>
            </div>

            {/* Task Filters */}
            <div className="inline-flex rounded-xl border border-slate-200 bg-slate-50 p-1">
              {(['all', 'pending', 'completed'] as FilterType[]).map((f) => (
                <button
                  key={f}
                  type="button"
                  onClick={() => setFilter(f)}
                  className={`rounded-lg px-3 py-1 text-xs font-semibold capitalize transition ${
                    filter === f
                      ? 'bg-white text-slate-950 shadow-sm'
                      : 'text-slate-600 hover:text-slate-950'
                  }`}
                >
                  {f === 'all' ? `All (${roadmap.tasks.length})` : f}
                </button>
              ))}
            </div>
          </div>

          {/* Task List */}
          <div className="space-y-3">
            <AnimatePresence mode="popLayout">
              {filteredTasks.length === 0 ? (
                <div className="rounded-2xl border border-dashed border-slate-200 p-8 text-center">
                  <p className="text-sm font-medium text-slate-500">No tasks in this category.</p>
                </div>
              ) : (
                filteredTasks.map((task, idx) => {
                  const isExpanded = expandedTaskIds.has(task.id);
                  const isToggling = togglingTaskId === task.id;

                  return (
                    <motion.div
                      key={task.id}
                      layout
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, scale: 0.96 }}
                      transition={{ duration: 0.2 }}
                      className={`group rounded-2xl border p-5 transition-all duration-200 ${
                        task.completed
                          ? 'border-emerald-200 bg-emerald-50/40'
                          : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-soft'
                      }`}
                    >
                      <div className="flex items-start gap-4">
                        {/* Interactive Toggle Checkbox */}
                        <button
                          type="button"
                          onClick={() => handleToggleTask(task)}
                          disabled={isToggling}
                          aria-label={task.completed ? 'Mark task as incomplete' : 'Mark task as complete'}
                          className={`mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-lg border transition-all ${
                            task.completed
                              ? 'border-emerald-600 bg-emerald-600 text-white shadow-sm'
                              : 'border-slate-300 bg-white hover:border-primary hover:bg-primary/5'
                          } ${isToggling ? 'opacity-50 cursor-wait' : 'cursor-pointer'}`}
                        >
                          {task.completed && <Check className="h-4 w-4 stroke-[3]" />}
                        </button>

                        <div className="min-w-0 flex-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <h3
                              className={`text-base font-semibold transition ${
                                task.completed ? 'text-slate-500 line-through' : 'text-slate-950'
                              }`}
                            >
                              {task.title}
                            </h3>
                            {task.due_date && (
                              <span className="inline-flex items-center gap-1 rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600">
                                <Clock className="h-3 w-3 text-slate-400" />
                                {task.due_date}
                              </span>
                            )}
                            <PriorityBadge priority={task.priority} />
                          </div>

                          {task.description && (
                            <div className="mt-2">
                              <p
                                className={`text-sm text-slate-600 leading-relaxed ${
                                  !isExpanded ? 'line-clamp-2' : ''
                                }`}
                              >
                                {task.description}
                              </p>
                              {task.description.length > 120 && (
                                <button
                                  type="button"
                                  onClick={() => toggleTaskExpansion(task.id)}
                                  className="mt-1.5 inline-flex items-center gap-1 text-xs font-semibold text-primary hover:underline"
                                >
                                  {isExpanded ? (
                                    <>
                                      Show less <ChevronUp className="h-3 w-3" />
                                    </>
                                  ) : (
                                    <>
                                      Read details <ChevronDown className="h-3 w-3" />
                                    </>
                                  )}
                                </button>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    </motion.div>
                  );
                })
              )}
            </AnimatePresence>
          </div>
        </section>

        {/* Right Column: Skill Gaps & Company Strategy */}
        <div className="space-y-6">
          {/* Skill Gaps Card */}
          <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft sm:p-7">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-500/10 text-amber-600">
                  <AlertTriangle className="h-5 w-5" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-slate-950">Identified Skill Gaps</h2>
                  <p className="text-xs text-slate-500">Areas prioritized for {roadmap.target_company}</p>
                </div>
              </div>
              <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-bold text-slate-700">
                {roadmap.skill_gaps.length} Gaps
              </span>
            </div>

            <div className="mt-5 space-y-3">
              {roadmap.skill_gaps.length === 0 ? (
                <p className="text-sm text-slate-500">No critical skill gaps identified. You are in great shape!</p>
              ) : (
                roadmap.skill_gaps.map((gap) => (
                  <div
                    key={gap.id}
                    className="rounded-2xl border border-slate-100 bg-slate-50/70 p-4 transition hover:bg-slate-50"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <p className="text-sm font-bold text-slate-950">{gap.skill_name}</p>
                      <SkillGapPriorityBadge priority={gap.priority} />
                    </div>
                    {gap.gap_description && (
                      <p className="mt-1.5 text-xs leading-relaxed text-slate-600">{gap.gap_description}</p>
                    )}
                  </div>
                ))
              )}
            </div>
          </section>

          {/* Company-Specific Recommendations */}
          {roadmap.company_recommendations && roadmap.company_recommendations.length > 0 && (
            <section className="rounded-[2rem] border border-indigo-100 bg-gradient-to-br from-indigo-50/50 via-white to-slate-50 p-6 shadow-soft sm:p-7">
              <div className="flex items-center gap-2.5">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
                  <BookOpen className="h-5 w-5" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-slate-950">{roadmap.target_company} Placement Strategy</h2>
                  <p className="text-xs text-slate-500">Key recommendations for selection rounds</p>
                </div>
              </div>

              <ul className="mt-5 space-y-3">
                {roadmap.company_recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start gap-3 rounded-2xl bg-white p-3.5 shadow-sm border border-slate-100">
                    <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-bold text-primary">
                      {index + 1}
                    </span>
                    <p className="text-xs sm:text-sm font-medium leading-relaxed text-slate-800">{rec}</p>
                  </li>
                ))}
              </ul>
            </section>
          )}
        </div>
      </div>
    </div>
  );
}

function PriorityBadge({ priority }: { priority: number }) {
  if (priority === 1) {
    return (
      <span className="rounded-md bg-rose-50 px-2 py-0.5 text-[11px] font-bold text-rose-700 border border-rose-200/60">
        High Priority
      </span>
    );
  }
  return (
    <span className="rounded-md bg-slate-100 px-2 py-0.5 text-[11px] font-medium text-slate-600">
      Priority {priority}
    </span>
  );
}

function SkillGapPriorityBadge({ priority }: { priority: number }) {
  if (priority === 1) {
    return (
      <span className="rounded-full bg-rose-100 px-2.5 py-0.5 text-[10px] font-bold text-rose-800">
        Critical Gap
      </span>
    );
  }
  return (
    <span className="rounded-full bg-amber-100 px-2.5 py-0.5 text-[10px] font-semibold text-amber-800">
      Moderate
    </span>
  );
}

function TrendingIcon({ percentage }: { percentage: number }) {
  if (percentage >= 75) {
    return <Sparkles className="h-4 w-4 text-emerald-500" />;
  }
  if (percentage >= 40) {
    return <Target className="h-4 w-4 text-indigo-500" />;
  }
  return <Compass className="h-4 w-4 text-slate-400" />;
}

function Compass(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <circle cx="12" cy="12" r="10" />
      <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" />
    </svg>
  );
}
