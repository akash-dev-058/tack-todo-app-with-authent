"use client";
export default function Loading() {
  return (
    <div className="flex items-center justify-center min-h-screen" role="status" aria-live="polite">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
    </div>
  );
}
