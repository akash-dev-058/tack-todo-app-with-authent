"use client";
export default function RegisterLoading() {
  return (
    <div className="flex items-center justify-center min-h-screen" role="status" aria-live="polite">
      <div className="animate-pulse text-gray-500">Loading registration…</div>
    </div>
  );
}
