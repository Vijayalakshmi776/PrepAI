import { Link } from 'react-router-dom';
import { Button } from '../../components/ui/Button';

export function LoginPanel() {
  return (
    <section className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-slate-950">Login to your PrepAI account</h2>
        <p className="text-sm text-slate-600">Continue your preparation journey with saved progress, AI recommendations, and personalized assessments.</p>
      </div>
      <form className="space-y-4 rounded-3xl border border-slate-200 bg-slate-50 p-6">
        <label className="block text-sm font-medium text-slate-800">
          Email
          <input type="email" className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10" placeholder="you@example.com" />
        </label>
        <label className="block text-sm font-medium text-slate-800">
          Password
          <input type="password" className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10" placeholder="Enter your password" />
        </label>
        <div className="flex items-center justify-between text-sm text-slate-600">
          <span>Don't have an account?</span>
          <Link to="register" className="font-semibold text-primary hover:text-secondary">Create one</Link>
        </div>
        <Button type="submit">Login</Button>
      </form>
    </section>
  );
}
