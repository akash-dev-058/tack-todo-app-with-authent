import { useAuth } from '@/context/auth-context';

/**
 * Convenience hook that returns authentication utilities.
 */
export function useAuthHook() {
  return useAuth();
}
