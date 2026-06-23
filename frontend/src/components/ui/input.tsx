import { InputHTMLAttributes, DetailedHTMLProps, forwardRef } from 'react';
import clsx from 'clsx';

type Props = DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement> & {
  className?: string;
};

const Input = forwardRef<HTMLInputElement, Props>(({ className, ...rest }, ref) => (
  <input
    ref={ref}
    className={clsx('rounded border border-gray-300 px-3 py-2 focus:border-primary focus:ring-primary focus:outline-none', className)}
    {...rest}
  />
));

Input.displayName = 'Input';
export default Input;
