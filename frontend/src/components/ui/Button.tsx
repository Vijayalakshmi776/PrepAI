import { Link } from 'react-router-dom';
import { ReactNode } from 'react';

interface ButtonProps {
  children: ReactNode;
  variant?: 'solid' | 'ghost';
  className?: string;
  to?: string;
  as?: typeof Link | 'button';
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  onClick?: () => void;
}

const baseStyles =
  'inline-flex items-center justify-center rounded-2xl px-5 py-3 text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-primary/40 disabled:cursor-not-allowed disabled:opacity-50';

const variants = {
  solid: 'bg-primary text-white hover:bg-secondary shadow-soft',
  ghost: 'bg-white/90 text-primary hover:bg-slate-100',
};

export function Button({
  children,
  variant = 'solid',
  className = '',
  to,
  as = 'button',
  type = 'button',
  disabled = false,
  onClick,
}: ButtonProps) {
  const styles = `${baseStyles} ${variants[variant]} ${className}`;

  if (as !== 'button' && to) {
    return (
      <Link to={to} className={styles}>
        {children}
      </Link>
    );
  }

  return (
    <button type={type} className={styles} disabled={disabled} onClick={onClick}>
      {children}
    </button>
  );
}
