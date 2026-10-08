import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../../components/ui/Button';
import { ProgressRing } from '../../components/ProgressRing';
import { useAuth } from '../../contexts/AuthContext';
import { onboardingApi } from '../../services/api';
import type { StudentProfile } from '../../types/profile';

export function DashboardPage() {
  const { user } = useAuth();
  const displayName = user?.full_name || user?.email || 'there';

  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [profileLoading, setProfileLoading] = useState(true);
  const [readinessScore, setReadinessScore] = useState(0);
  const [roadmapProgress, setRoadmapProgress] = useState(0);
  const [strongestSkill, setStrongestSkill] = useState('Communication');
  const [weakestSkill, setWeakestSkill] = useState('Data Structures');

  useEffect(() => {
    let cancelled = false;
    onboardingApi
      .getMyProfile()
      .then((data) => {
        if (!cancelled) setProfile(data);
      })
      .catch(() => {
        if (!cancelled) setProfile(null);
      })
      .finally(() => {
        if (!cancelled) setProfileLoading(false);
      });

    import('../../services/api').then(({ roadmapApi, resumeApi }) => {
      roadmapApi.getMyRoadmap().then((data) => {
        if (!cancelled) {
          setReadinessScore(data.progress.readiness_score || 0);
          setRoadmapProgress(data.progress.completion_percentage || 0);
        }
      }).catch(() => {
        if (!cancelled) {
          setReadinessScore(0);
          setRoadmapProgress(0);
        }
      });

      resumeApi.getLatestAnalysis().then((resume) => {
        if (!cancelled && resume.detected_skills && resume.detected_skills.length > 0) {
          setStrongestSkill(resume.detected_skills[0]);
          if (resume.missing_skills && resume.missing_skills.length > 0) {
            setWeakestSkill(resume.missing_skills[0]);
          }
        }
      }).catch(() => {});
    });

    return () => {
      cancelled = true;
    };
  }, []);

  const targetCompany = profile?.target_company ?? '—';
  const targetRole = profile?.target_role ?? '—';
  const currentLevel = profile?.current_level ?? '—';
  const careerGoal = profile?.career_goal ?? '—';

  return (
    <div className="grid gap-8 xl:grid-cols-[0.95fr_0.5fr]">
      <section className="space-y-8 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Welcome back, {displayName}</p>
            <h1 className="text-3xl font-bold text-slate-950">Your AI placement mentor dashboard</h1>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <Button as={Link} to="/resume" variant="outline" className="border-slate-300 hover:bg-slate-50">
              Resume Analysis
            </Button>
            <Button as={Link} to="/roadmap" variant="outline" className="border-slate-300 hover:bg-slate-50">
              View Roadmap
            </Button>
            <Button as={Link} to="/interview" className="min-w-[170px]">
              Mock Interview
            </Button>
          </div>
        </div>

        <div className="grid gap-6 xl:grid-cols-[1.3fr_1fr]">
          <div className="rounded-[1.75rem] border border-slate-200 bg-slate-50 p-8">
            <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Placement readiness</p>
                <p className="mt-2 text-5xl font-black text-slate-950">{Math.round(readinessScore)}%</p>
              </div>
              <div className="rounded-3xl bg-white p-5 shadow-sm">
                <ProgressRing progress={Math.round(readinessScore)} label="Readiness" />
              </div>
            </div>
            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              {profileLoading ? (
                <div className="col-span-2 rounded-3xl border border-slate-200 bg-white p-5">
                  <p className="text-sm text-slate-500">Loading your profile…</p>
                </div>
              ) : (
                [
                  { label: 'Target Company', value: targetCompany },
                  { label: 'Target Role', value: targetRole },
                  { label: 'Current Level', value: currentLevel },
                  { label: 'Career Goal', value: careerGoal },
                ].map((item) => (
                  <div key={item.label} className="rounded-3xl border border-slate-200 bg-white p-5">
                    <p className="text-sm text-slate-500">{item.label}</p>
                    <p className="mt-2 text-base font-semibold text-slate-950">{item.value}</p>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="space-y-6 rounded-[1.75rem] border border-slate-200 bg-slate-50 p-8">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Skill snapshot</p>
              <p className="mt-2 text-lg font-semibold text-slate-950">Top Skill: {strongestSkill}</p>
              <p className="text-sm text-slate-600">Focus Area: {weakestSkill}</p>
            </div>
            <div className="space-y-4">
              <div className="rounded-3xl bg-white p-5 shadow-sm">
                <p className="text-sm text-slate-500">Recent assessment</p>
                <p className="mt-2 text-base font-semibold text-slate-900">Initial assessment complete</p>
              </div>
              <Link to="/roadmap" className="block rounded-3xl bg-white p-5 shadow-sm transition hover:shadow-md">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-slate-500">Personalized Roadmap</p>
                  <span className="text-xs font-semibold text-primary">{Math.round(roadmapProgress)}% complete &rarr;</span>
                </div>
                <div className="mt-3 h-3 overflow-hidden rounded-full bg-slate-200">
                  <div
                    className="h-full rounded-full bg-primary transition-all duration-500"
                    style={{ width: `${Math.min(Math.max(roadmapProgress, 0), 100)}%` }}
                  />
                </div>
                <p className="mt-2 text-sm text-slate-600">Track tasks & company-specific skills</p>
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="space-y-6 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">AI recommendation</p>
            <h2 className="mt-2 text-2xl font-bold text-slate-950">
              {targetCompany !== '—'
                ? `Focus on practical coding & SQL fundamentals this week`
                : 'Complete onboarding to get personalized recommendations'}
            </h2>
          </div>
          {targetCompany !== '—' && (
            <span className="rounded-3xl bg-primary/10 px-4 py-2 text-sm font-semibold text-primary">
              Company pattern: {targetCompany}
            </span>
          )}
        </div>
        <div className="grid gap-4">
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm text-slate-500">Recommended action</p>
            <p className="mt-3 text-base font-semibold text-slate-950">
              {targetCompany !== '—'
                ? `Complete 2 aptitude drills and 2 coding problems tailored for ${targetCompany} selection rounds.`
                : 'Complete your onboarding to unlock company-specific recommendations.'}
            </p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm text-slate-500">Next milestone</p>
            <p className="mt-3 text-base font-semibold text-slate-950">
              Prepare for the next mock interview with medium difficulty.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
