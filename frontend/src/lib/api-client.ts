import { z } from 'zod';

/**
 * Typed wrapper around fetch that automatically includes credentials and base URL.
 * Throws a typed error with status and message for non‑2xx responses.
 */
export class ApiError extends Error {
  status: number;
  data: unknown;
  constructor(status: number, data: unknown) {
    super(`API Error ${status}`);
    this.status = status;
    this.data = data;
    Object.setPrototypeOf(this, ApiError.prototype);
  }
}

const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL?.replace(/\/+$/, '') || '';

interface RequestOptions<T> {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: T;
  schema?: z.ZodSchema<any>;
  params?: Record<string, string | number>;
}

export async function apiRequest<T = any, R = any>(
  endpoint: string,
  { method = 'GET', body, schema, params }: RequestOptions<T> = {}
): Promise<R> {
  try {
    const url = new URL(`${BASE_URL}${endpoint}`);
    if (params) {
      Object.entries(params).forEach(([k, v]) => url.searchParams.append(k, String(v)));
    }
    const response = await fetch(url.toString(), {
      method,
      credentials: 'include', // send HttpOnly cookies
      headers: {
        'Content-Type': 'application/json'
      },
      body: body ? JSON.stringify(body) : undefined
    });

    const contentType = response.headers.get('content-type');
    const isJson = contentType?.includes('application/json');
    const data = isJson ? await response.json() : await response.text();

    if (!response.ok) {
      throw new ApiError(response.status, data);
    }

    if (schema) {
      const parsed = schema.safeParse(data);
      if (!parsed.success) {
        console.error('API response validation failed', parsed.error);
        throw new Error('Invalid API response');
      }
      return parsed.data as R;
    }
    return data as R;
  } catch (err) {
    if (err instanceof ApiError) {
      // Re‑throw for callers to handle
      throw err;
    }
    console.error('Network or unexpected error', err);
    throw new Error('Network error');
  }
}
