import Link from 'next/link';
import { useAuth } from '@/context/auth-context';
import Button from '@/components/ui/button';
import { useState } from 'react';
import { MenuIcon, XIcon } from '@/components/ui/icons';

export default function Navbar() {
  const { user, logout, loading } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const toggleMobile = () => setMobileOpen(!mobileOpen);

  return (
    <nav className="bg-white border-b border-gray-200" role="navigation" aria-label="Main navigation">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link href="/" className="text-xl font-bold text-primary">
            AuthTodoPro
          </Link>
          <div className="hidden md:flex space-x-4 items-center">
            {user ? (
              <>
                <span className="text-gray-700">{user.email}</span>
                <Button variant="ghost" onClick={() => logout()} disabled={loading}>
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Link href="/login" className="text-primary hover:underline">
                  Login
                </Link>
                <Link href="/register" className="text-primary hover:underline">
                  Register
                </Link>
              </>
            )}
          </div>
          <div className="md:hidden flex items-center">
            <Button variant="ghost" onClick={toggleMobile} aria-label="Toggle menu">
              {mobileOpen ? <XIcon /> : <MenuIcon />}
            </Button>
          </div>
        </div>
      </div>
      {mobileOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {user ? (
              <>
                <span className="block px-3 py-2 text-gray-700">{user.email}</span>
                <Button variant="ghost" onClick={() => logout()} disabled={loading} className="block w-full text-left px-3 py-2">
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Link href="/login" className="block px-3 py-2 text-primary hover:bg-gray-100">
                  Login
                </Link>
                <Link href="/register" className="block px-3 py-2 text-primary hover:bg-gray-100">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
