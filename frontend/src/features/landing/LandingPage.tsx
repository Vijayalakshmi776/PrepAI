import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Button } from '../../components/ui/Button';

const features = [
  {
    title: 'Company-specific preparation',
    description: 'AI adapts your journey to the chosen company interview pattern, not a generic checklist.',
  },
  {
    title: 'Mock interview mentor',
    description: 'Text-based AI interviews that adapt to your answers and maintain realistic context.',
  },
  {
    title: 'Resume analysis',
    description: 'AI reviews your resume for keywords, experience fit, and missing role-specific skills.',
  },
  {
    title: 'Personalized roadmap',
    description: 'A dynamic learning plan built from your profile, assessment results, and interview feedback.',
  },
];

export function LandingPage() {
  return (
    <section className="space-y-16 pb-16 pt-10">
      <div className="grid gap-12 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
        <div className="space-y-8">
          <div className="inline-flex items-center gap-2 rounded-full border border-primary/15 bg-primary/5 px-4 py-2 text-sm font-semibold text-primary shadow-sm">
            AI-driven placement mentor for future-ready careers
          </div>
          <div className="space-y-6">
            <h1 className="max-w-3xl text-4xl font-bold tracking-tight text-slate-950 sm:text-5xl">
              PrepAI helps you practice smart and become placement ready.
            </h1>
            <p className="max-w-2xl text-lg text-slate-600 sm:text-xl">
              Personalized company-specific journeys, realistic mock interviews, resume insights, and progress tracking for every aspiring professional.
            </p>
          </div>

          <div className="flex flex-col gap-4 sm:flex-row">
            <Button as={Link} to="/auth/register">Start Preparing</Button>
            <Button as="button" variant="ghost" className="text-primary">Explore Features</Button>
          </div>
        </div>

        <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
          <div className="space-y-4">
            <div className="rounded-3xl bg-gradient-to-br from-primary/10 via-secondary/5 to-white p-6">
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Student journey</p>
              <div className="mt-6 space-y-4">
                {['Profile', 'Assessment', 'AI Analysis', 'Mock Interview', 'Feedback', 'Ready'].map((step) => (
                  <div key={step} className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary/10 text-primary">✓</div>
                    <span className="text-sm font-medium text-slate-800">{step}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              {features.map((feature) => (
                <article key={feature.title} className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
                  <h3 className="text-base font-semibold text-slate-900">{feature.title}</h3>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{feature.description}</p>
                </article>
              ))}
            </div>
          </div>
        </div>
      </div>

      <section id="how-it-works" className="rounded-[2rem] bg-white p-8 shadow-soft">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">How it works</p>
            <h2 className="mt-3 text-3xl font-bold text-slate-950">A guided preparation loop built around your goals.</h2>
          </div>
          <p className="max-w-2xl text-sm leading-7 text-slate-600">
            Onboarding learns your profile, the AI generates a company-specific roadmap, assessments create a baseline, and mock interviews sharpen your readiness over time.
          </p>
        </div>
      </section>
    </section>
  );
}
