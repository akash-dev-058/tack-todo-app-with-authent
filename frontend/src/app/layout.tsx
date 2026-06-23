import '@/app/globals.css';
import { ReactNode } from 'react';
import { AuthProvider } from '@/context/auth-context';
import { QueryProvider } from '@/components/providers/query-provider';

/**
 * Root layout that wraps every page with global providers.
 */
export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="h-full bg-gray-50">
      <head>
        <title>AuthTodoPro</title>
        <meta name="description" content="Secure Todo app with real‑time sync" />
      </head>
      <body className="flex flex-col min-h-screen">
        <AuthProvider>
          <QueryProvider>
            <main className="flex-1 container mx-auto px-4 py-6" role="main">
              {children}
            </main>
          </QueryProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
