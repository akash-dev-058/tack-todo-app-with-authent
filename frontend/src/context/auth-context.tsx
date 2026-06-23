import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { apiRequest, ApiError } from '@/lib/api-client';
import { z } from 'zod';

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextProps {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
  refresh: () => Promise<void>;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

const userSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  name: z.string().optional()
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchCurrentUser = async () => {
    try {
      const data = await apiRequest('/api/v1/users/me', { schema: userSchema });
      setUser(data);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        setUser(null);
      } else {
        console.error('Failed to fetch current user', err);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      await apiRequest('/api/v1/auth/login', {
        method: 'POST',
        body: { email, password }
      });
      await fetchCurrentUser();
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string, name?: string) => {
    setLoading(true);
    try {
      await apiRequest('/api/v1/auth/register', {
        method: 'POST',
        body: { email, password, name }
      });
      await fetchCurrentUser();
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await apiRequest('/api/v1/auth/logout', { method: 'POST' });
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const refresh = async () => {
    try {
      await apiRequest('/api/v1/auth/refresh', { method: 'POST' });
      await fetchCurrentUser();
    } catch (err) {
      console.error('Token refresh failed', err);
    }
  };

  const value: AuthContextProps = {
    user,
    loading,
    login,
    register,
    logout,
    refresh
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return ctx;
}
