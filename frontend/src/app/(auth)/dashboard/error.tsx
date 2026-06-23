"use client";
import Button from '@/components/ui/button';

interface Props {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function DashboardError({ error, reset }: Props) {
  return (
    <div className="p-4 text-center">
      <h2 className="text-xl font-semibold mb-2">Failed to load dashboard</h2>
      <p className="mb-4 text-gray-600">{error.message}</p>
      <Button onClick={reset}>Retry</Button>
    </div>
  );
}
