import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../../components/ui/Button';
import { authApi } from '../../services/api';

export function RegisterPanel() {
  const navigate = useNavigate();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);

    if (!fullName.trim() || !email.trim() || !password.trim()) {
      setError('Please complete all fields before continuing.');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }

    setIsSubmitting(true);
    try {
      await authApi.register({ email, full_name: fullName, password });
      navigate('/auth/login');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to create your account.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-slate-950">Create your PrepAI account</h2>
        <p className="text-sm text-slate-600">Start with onboarding to build a company-specific placement plan and AI mentor experience.</p>
      </div>
      <form className="space-y-4 rounded-3xl border border-slate-200 bg-slate-50 p-6" onSubmit={handleSubmit}>
        <label className="block text-sm font-medium text-slate-800">
          Full name
          <input type="text" value={fullName} onChange={(event) => setFullName(event.target.value)} className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10" placeholder="Your full name" />
        </label>
        <label className="block text-sm font-medium text-slate-800">
          Email
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10" placeholder="you@example.com" />
        </label>
        <label className="block text-sm font-medium text-slate-800">
          Password
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10" placeholder="Create a password" />
        </label>
        {error ? <p className="text-sm font-medium text-rose-600">{error}</p> : null}
        <div className="flex items-center justify-between text-sm text-slate-600">
          <span>Already a member?</span>
          <Link to="login" className="font-semibold text-primary hover:text-secondary">Login</Link>
        </div>
        <Button type="submit" className={isSubmitting ? 'opacity-70' : ''}>{isSubmitting ? 'Creating account...' : 'Register'}</Button>
      </form>
    </section>
  );
}
