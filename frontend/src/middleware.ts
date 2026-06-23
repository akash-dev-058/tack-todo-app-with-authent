import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * Middleware that protects routes under /dashboard and any other auth‑required paths.
 * It checks for the presence of a valid session cookie by calling the backend.
 */
export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const protectedRoutes = ['/dashboard'];
  const isProtected = protectedRoutes.some((r) => pathname.startsWith(r));

  if (!isProtected) {
    return NextResponse.next();
  }

  try {
    const apiResponse = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/users/me`,
      { credentials: 'include' }
    );
    if (apiResponse.ok) {
      return NextResponse.next();
    }
    // Not authenticated – redirect to login preserving the original path
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('next', pathname);
    return NextResponse.redirect(loginUrl);
  } catch (err) {
    console.error('Auth middleware error', err);
    const fallbackUrl = new URL('/login', request.url);
    return NextResponse.redirect(fallbackUrl);
  }
}

export const config = {
  matcher: ['/dashboard/:path*']
};
