"use client";
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Button from '@/components/ui/button';

interface Props {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function GlobalError({ error, reset }: Props) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  const router = useRouter();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Something went wrong</h1>
      <p className="mb-4 text-gray-700">{error.message}</p>
      <div className="flex space-x-2">
        <Button onClick={reset}>Try again</Button>
        <Button variant="ghost" onClick={() => router.push('/')}>Home</Button>
      </div>
    </div>
  );
}
