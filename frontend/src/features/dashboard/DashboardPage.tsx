import { motion } from 'framer-motion';
import { Button } from '../../components/ui/Button';
import { ProgressRing } from '../../components/ProgressRing';

export function DashboardPage() {
  return (
    <div className="grid gap-8 xl:grid-cols-[0.95fr_0.5fr]">
      <section className="space-y-8 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Good morning, keep improving</p>
            <h1 className="text-3xl font-bold text-slate-950">Your AI placement mentor dashboard</h1>
          </div>
          <Button as={Button} to="/interview" className="min-w-[180px]">Start mock interview</Button>
        </div>

        <div className="grid gap-6 xl:grid-cols-[1.3fr_1fr]">
          <div className="rounded-[1.75rem] border border-slate-200 bg-slate-50 p-8">
            <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Placement readiness</p>
                <p className="mt-2 text-5xl font-black text-slate-950">63%</p>
              </div>
              <div className="rounded-3xl bg-white p-5 shadow-sm">
                <ProgressRing progress={63} label="Readiness" />
              </div>
            </div>
            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              {[
                { label: 'Target Company', value: 'TCS' },
                { label: 'Target Role', value: 'Software Engineer' },
                { label: 'Current Level', value: 'Intermediate' },
                { label: 'Today’s action', value: 'Practice 3 easy coding problems' },
              ].map((item) => (
                <div key={item.label} className="rounded-3xl border border-slate-200 bg-white p-5">
                  <p className="text-sm text-slate-500">{item.label}</p>
                  <p className="mt-2 text-base font-semibold text-slate-950">{item.value}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-6 rounded-[1.75rem] border border-slate-200 bg-slate-50 p-8">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Skill snapshot</p>
              <p className="mt-2 text-lg font-semibold text-slate-950">Strongest: Communication</p>
              <p className="text-sm text-slate-600">Weakest: Data Structures</p>
            </div>
            <div className="space-y-4">
              <div className="rounded-3xl bg-white p-5 shadow-sm">
                <p className="text-sm text-slate-500">Recent assessment</p>
                <p className="mt-2 text-base font-semibold text-slate-900">Initial assessment complete</p>
              </div>
              <div className="rounded-3xl bg-white p-5 shadow-sm">
                <p className="text-sm text-slate-500">Progress</p>
                <div className="mt-3 h-3 overflow-hidden rounded-full bg-slate-200">
                  <div className="h-full w-2/5 rounded-full bg-primary transition-all duration-500" />
                </div>
                <p className="mt-2 text-sm text-slate-600">40% of your personalized roadmap completed</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="space-y-6 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">AI recommendation</p>
            <h2 className="mt-2 text-2xl font-bold text-slate-950">Focus on practical coding & SQL fundamentals this week</h2>
          </div>
          <span className="rounded-3xl bg-primary/10 px-4 py-2 text-sm font-semibold text-primary">Company pattern: TCS</span>
        </div>
        <div className="grid gap-4">
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm text-slate-500">Recommended action</p>
            <p className="mt-3 text-base font-semibold text-slate-950">Complete 2 aptitude drills and 2 coding problems tailored for TCS selection rounds.</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm text-slate-500">Next milestone</p>
            <p className="mt-3 text-base font-semibold text-slate-950">Prepare for the next mock interview with medium difficulty.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
