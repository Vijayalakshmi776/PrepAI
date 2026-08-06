import { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '../../components/ui/Button';

const steps = [
  {
    id: 'userType',
    question: 'What best describes you?',
    options: ['College Student', 'Graduate', 'Job Seeker'],
  },
  {
    id: 'careerGoal',
    question: 'What are you preparing for?',
    options: ['Placement', 'First Job', 'Internship', 'Career Switch', 'General Interview Preparation'],
  },
  {
    id: 'companyType',
    question: 'What type of company are you targeting?',
    options: ['Service-based', 'Product-based', 'Startup', 'Not Sure'],
  },
  {
    id: 'dreamCompany',
    question: 'Which company are you preparing for?',
    options: ['TCS', 'Infosys', 'Cognizant', 'Accenture', 'Zoho', 'Freshworks', 'Amazon', 'Microsoft', 'Google', 'Adobe', 'Oracle', 'Startup', 'Other', 'Not Decided'],
  },
  {
    id: 'targetRole',
    question: 'What role are you targeting?',
    options: ['Software Engineer', 'Frontend Developer', 'Backend Developer', 'Full Stack Developer', 'Python Developer', 'Java Developer', 'Data Analyst', 'Data Scientist', 'AI/ML Engineer', 'UI/UX Designer', 'Other'],
  },
  {
    id: 'level',
    question: 'How would you describe your current level?',
    options: ['Beginner', 'Intermediate', 'Advanced'],
  },
  {
    id: 'skills',
    question: 'Which skills are you comfortable with?',
    options: ['Python', 'Java', 'JavaScript', 'React', 'HTML/CSS', 'SQL', 'C/C++', 'Data Structures', 'Machine Learning', 'AI', 'Communication', 'Aptitude', 'Problem Solving'],
    multi: true,
  },
];

export function OnboardingPage() {
  const [stepIndex, setStepIndex] = useState(0);
  const [values, setValues] = useState<Record<string, string | string[]>>({});

  const step = steps[stepIndex];

  const selectOption = (option: string) => {
    setValues((current) => {
      if (step.multi) {
        const currentValues = Array.isArray(current[step.id]) ? current[step.id] : [];
        const nextValues = currentValues.includes(option)
          ? (currentValues.filter((value) => value !== option) as string[])
          : ([...currentValues, option] as string[]);
        return { ...current, [step.id]: nextValues };
      }

      return { ...current, [step.id]: option };
    });
  };

  const selected = values[step.id];
  const isNextEnabled = step.multi ? Array.isArray(selected) && selected.length > 0 : typeof selected === 'string';

  return (
    <div className="mx-auto max-w-5xl rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft sm:p-10">
      <div className="mb-8 flex flex-col gap-3">
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Onboarding</p>
        <h1 className="text-3xl font-bold text-slate-950">Let’s tailor your PrepAI journey.</h1>
        <p className="max-w-2xl text-sm leading-7 text-slate-600">
          Answer a few quick questions so the platform can recommend company-specific practice, interview patterns, and career-ready feedback.
        </p>
      </div>

      <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-8">
        <div className="mb-6 flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-slate-800">Step {stepIndex + 1} of {steps.length}</p>
            <h2 className="mt-2 text-2xl font-bold text-slate-950">{step.question}</h2>
          </div>
          <p className="text-sm text-slate-600">Select {step.multi ? 'all that apply' : 'one option'}</p>
        </div>

        <motion.div layout className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {step.options.map((option) => {
            const isActive = step.multi ? Array.isArray(selected) && selected.includes(option) : selected === option;
            return (
              <button
                key={option}
                type="button"
                onClick={() => selectOption(option)}
                className={`rounded-3xl border px-5 py-4 text-left transition ${isActive ? 'border-primary bg-primary/10 text-primary' : 'border-slate-200 bg-white text-slate-700 hover:border-primary/60 hover:bg-slate-50'}`}
              >
                <span className="block text-base font-semibold">{option}</span>
              </button>
            );
          })}
        </motion.div>

        <div className="mt-8 flex items-center justify-between gap-4">
          <button
            type="button"
            disabled={stepIndex === 0}
            onClick={() => setStepIndex((index) => Math.max(0, index - 1))}
            className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-primary hover:text-primary disabled:cursor-not-allowed disabled:opacity-50"
          >
            Back
          </button>
          <Button
            type="button"
            className="min-w-[160px]"
            disabled={!isNextEnabled}
            onClick={() => {
              if (stepIndex < steps.length - 1) {
                setStepIndex((index) => index + 1);
              }
            }}
          >
            {stepIndex === steps.length - 1 ? 'Finish onboarding' : 'Next question'}
          </Button>
        </div>
      </div>

      {stepIndex === steps.length - 1 && (
        <div className="mt-10 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-xl font-semibold text-slate-950">Onboarding summary</h3>
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            {Object.entries(values).map(([key, value]) => (
              <div key={key} className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                <p className="text-sm uppercase tracking-[0.2em] text-slate-500">{key.replace(/([A-Z])/g, ' $1')}</p>
                <p className="mt-2 text-sm leading-6 text-slate-700">{Array.isArray(value) ? value.join(', ') : value}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
