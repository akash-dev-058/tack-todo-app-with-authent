import { ReactNode } from 'react';
import '@/app/globals.css';

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="h-full bg-gray-50">
      <head>
        <title>AuthTodoPro</title>
      </head>
      <body className="min-h-screen flex flex-col">
        {children}
      </body>
    </html>
  );
}
