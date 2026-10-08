import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/Button';

const landingNavItems = [
  { label: 'Features', href: '/#features' },
  { label: 'How It Works', href: '/#how-it-works' },
  { label: 'Companies', href: '/#companies' },
];

const appNavItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Roadmap', to: '/roadmap' },
  { label: 'Mock Interview', to: '/interview' },
  { label: 'Resume Analysis', to: '/resume' },
];

export function Navbar() {
  const navigate = useNavigate();
  const { isAuthenticated, logout, user } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/auth/login');
  };

  return (
    <header className="border-b border-border bg-white/90 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-4 py-4 sm:px-6 lg:px-8">
        <Link to={isAuthenticated ? '/dashboard' : '/'} className="flex items-center gap-3 text-lg font-semibold text-primary">
          <span className="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-secondary text-white shadow-soft">
            P
          </span>
          PREPAI
        </Link>

        <nav className="hidden items-center gap-6 md:flex">
          {isAuthenticated
            ? appNavItems.map((item) => (
                <Link
                  key={item.label}
                  to={item.to}
                  className="text-sm font-semibold text-slate-700 transition hover:text-primary"
                >
                  {item.label}
                </Link>
              ))
            : landingNavItems.map((item) => (
                <a
                  key={item.label}
                  href={item.href}
                  className="text-sm font-medium text-secondary transition hover:text-primary"
                >
                  {item.label}
                </a>
              ))}
        </nav>

        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <>
              <span className="hidden text-sm font-medium text-slate-600 sm:block">{user?.full_name || user?.email}</span>
              <button type="button" onClick={handleLogout} className="text-sm font-medium text-secondary transition hover:text-primary">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/auth/login" className="text-sm font-medium text-secondary transition hover:text-primary">
                Login
              </Link>
              <Button as={Link} to="/auth/register" variant="solid">
                Get Started
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
