import { ButtonHTMLAttributes, DetailedHTMLProps, ReactNode } from 'react';
import clsx from 'clsx';

interface Props extends DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
}

export default function Button({ children, className, variant = 'primary', disabled, ...rest }: Props) {
  const base = 'inline-flex items-center justify-center rounded px-4 py-2 text-sm font-medium transition-colors duration-150 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2';
  const variants = {
    primary: 'bg-primary text-white hover:bg-primary/90 focus-visible:ring-primary',
    secondary: 'bg-secondary text-white hover:bg-secondary/90 focus-visible:ring-secondary',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500',
    ghost: 'bg-transparent text-primary hover:bg-primary/10 focus-visible:ring-primary'
  };
  const disabledStyle = disabled ? 'opacity-50 cursor-not-allowed' : '';
  return (
    <button
      className={clsx(base, variants[variant], disabledStyle, className)}
      disabled={disabled}
      {...rest}
    >
      {children}
    </button>
  );
}
