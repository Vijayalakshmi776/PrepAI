import { Link } from 'react-router-dom';
import { Button } from './ui/Button';

const navItems = [
  { label: 'Features', href: '#features' },
  { label: 'How It Works', href: '#how-it-works' },
  { label: 'Companies', href: '#companies' },
  { label: 'About', href: '#about' },
];

export function Navbar() {
  return (
    <header className="border-b border-border bg-white/90 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-4 py-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-3 text-lg font-semibold text-primary">
          <span className="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-secondary text-white shadow-soft">
            P
          </span>
          PREPAI
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          {navItems.map((item) => (
            <a key={item.label} href={item.href} className="text-sm font-medium text-secondary transition hover:text-primary">
              {item.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <Link to="/auth/login" className="text-sm font-medium text-secondary transition hover:text-primary">
            Login
          </Link>
          <Button as={Link} to="/auth/register" variant="solid">
            Get Started
          </Button>
        </div>
      </div>
    </header>
  );
}
