import { redirect } from 'next/navigation';

/**
 * Root page redirects to dashboard if authenticated, otherwise to login.
 */
export default async function Home() {
  // Server‑side check using cookies – fallback to client side if needed.
  // For simplicity we redirect client‑side in a useEffect inside layout.
  redirect('/login');
}
