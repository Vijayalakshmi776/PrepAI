import { Link, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { LoginPanel } from './LoginPanel';
import { RegisterPanel } from './RegisterPanel';

export function AuthPage() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div className="py-12 text-center text-sm text-slate-600">Loading session...</div>;
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="mx-auto flex w-full max-w-4xl flex-col gap-10 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-soft sm:p-10">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Welcome to PrepAI</p>
          <h1 className="mt-2 text-3xl font-bold text-slate-950">Your personal placement mentor starts here.</h1>
        </div>
        <div className="flex items-center gap-4 text-sm text-slate-600">
          <Link to="login" className="font-semibold text-primary hover:text-secondary">Login</Link>
          <Link to="register" className="font-semibold text-primary hover:text-secondary">Register</Link>
        </div>
      </div>

      <Routes>
        <Route path="login" element={<LoginPanel />} />
        <Route path="register" element={<RegisterPanel />} />
        <Route path="*" element={<Navigate to="login" replace />} />
      </Routes>
    </div>
  );
}
