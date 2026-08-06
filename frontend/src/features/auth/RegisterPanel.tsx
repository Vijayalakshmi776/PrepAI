import { Link } from 'react-router-dom';
import { Button } from '../../components/ui/Button';

export function RegisterPanel() {
  return (
    <section className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-slate-950">Create your PrepAI account</h2>
        <p className="text-sm text-slate-600">Start with onboarding to build a company-specific placement plan and AI mentor experience.</p>
      </div>
      <form className="space-y-4 rounded-3xl border border-slate-200 bg-slate-50 p-6">
        <label className="block text-sm font-medium text-slate-800">
          Full name
          <input type="text" className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10" placeholder="Your full name" />
        </label>
        <label className="block text-sm font-medium text-slate-800">
          Email
          <input type="email" className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10" placeholder="you@example.com" />
        </label>
        <label className="block text-sm font-medium text-slate-800">
          Password
          <input type="password" className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10" placeholder="Create a password" />
        </label>
        <div className="flex items-center justify-between text-sm text-slate-600">
          <span>Already a member?</span>
          <Link to="login" className="font-semibold text-primary hover:text-secondary">Login</Link>
        </div>
        <Button type="submit">Register</Button>
      </form>
    </section>
  );
}
