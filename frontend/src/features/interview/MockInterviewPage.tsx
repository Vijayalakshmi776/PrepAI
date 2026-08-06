import { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '../../components/ui/Button';

const interviewOptions = ['Easy', 'Medium', 'Difficult'];

export function MockInterviewPage() {
  const [company, setCompany] = useState('TCS');
  const [role, setRole] = useState('Software Engineer');
  const [difficulty, setDifficulty] = useState('Medium');
  const [started, setStarted] = useState(false);
  const [transcript, setTranscript] = useState<string[]>(['The AI interviewer will ask one question at a time.']);

  const beginInterview = () => {
    setStarted(true);
    setTranscript([`You are starting a ${difficulty} mock interview for ${company} as a ${role}.`, 'Question 1: Explain your approach to solving a coding problem with constraints.']);
  };

  return (
    <div className="space-y-10 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft">
      <div className="space-y-3">
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">AI mock interview</p>
        <h1 className="text-3xl font-bold text-slate-950">Practice with company-specific interview flow.</h1>
        <p className="max-w-3xl text-sm leading-7 text-slate-600">
          Start an adaptive interview that evaluates your communication, technical reasoning, and problem-solving in real time.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <label className="block rounded-3xl border border-slate-200 bg-slate-50 p-5">
          <span className="text-sm font-semibold text-slate-700">Company</span>
          <select value={company} onChange={(event) => setCompany(event.target.value)} className="mt-3 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10">
            {['TCS', 'Infosys', 'Zoho', 'Amazon', 'Startup'].map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </label>

        <label className="block rounded-3xl border border-slate-200 bg-slate-50 p-5">
          <span className="text-sm font-semibold text-slate-700">Role</span>
          <select value={role} onChange={(event) => setRole(event.target.value)} className="mt-3 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10">
            {['Software Engineer', 'Frontend Developer', 'Backend Developer', 'Full Stack Developer'].map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </label>

        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
          <p className="text-sm font-semibold text-slate-700">Difficulty</p>
          <div className="mt-3 flex flex-wrap gap-3">
            {interviewOptions.map((option) => (
              <button
                key={option}
                type="button"
                onClick={() => setDifficulty(option)}
                className={`rounded-full border px-4 py-2 text-sm font-semibold transition ${difficulty === option ? 'border-primary bg-primary/10 text-primary' : 'border-slate-200 bg-white text-slate-700 hover:border-primary hover:bg-slate-50'}`}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      </div>

      <Button onClick={beginInterview}>Start Interview</Button>

      {started && (
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-4 rounded-[2rem] border border-slate-200 bg-slate-50 p-6">
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Interview transcript</p>
          <div className="space-y-3">
            {transcript.map((line, index) => (
              <p key={index} className="rounded-3xl border border-slate-200 bg-white p-4 text-sm leading-6 text-slate-700">{line}</p>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
