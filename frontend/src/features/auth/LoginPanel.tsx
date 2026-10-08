import { FormEvent, useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Button } from '../../components/ui/Button';
import { useAuth } from '../../contexts/AuthContext';
import { authApi, onboardingApi } from '../../services/api';

export function LoginPanel() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const from = (location.state as { from?: { pathname: string } } | null)?.from?.pathname;

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);

    if (!email.trim() || !password.trim()) {
      setError('Please enter both email and password.');
      return;
    }

    setIsSubmitting(true);
    try {
      const tokens = await authApi.login({ email, password });
      await login(tokens);

      if (from && from !== '/auth/login' && from !== '/auth/register') {
        navigate(from, { replace: true });
        return;
      }

      try {
        const profile = await onboardingApi.getMyProfile();
        if (profile && profile.target_role) {
          navigate('/dashboard', { replace: true });
        } else {
          navigate('/onboarding', { replace: true });
        }
      } catch {
        navigate('/onboarding', { replace: true });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to log in.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-slate-950">Login to your PrepAI account</h2>
        <p className="text-sm text-slate-600">Continue your preparation journey with saved progress, AI recommendations, and personalized assessments.</p>
      </div>
      <form className="space-y-4 rounded-3xl border border-slate-200 bg-slate-50 p-6" onSubmit={handleSubmit}>
        <label className="block text-sm font-medium text-slate-800">
          Email
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10" placeholder="you@example.com" />
        </label>
        <label className="block text-sm font-medium text-slate-800">
          Password
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10" placeholder="Enter your password" />
        </label>
        {error ? <p className="text-sm font-medium text-rose-600">{error}</p> : null}
        <div className="flex items-center justify-between text-sm text-slate-600">
          <span>Don't have an account?</span>
          <Link to="register" className="font-semibold text-primary hover:text-secondary">Create one</Link>
        </div>
        <Button type="submit" className={isSubmitting ? 'opacity-70' : ''}>{isSubmitting ? 'Logging in...' : 'Login'}</Button>
      </form>
    </section>
  );
}
