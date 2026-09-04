'use client';

import Link from 'next/link';
import { useSession, signOut } from 'next-auth/react';
import Button from '@/components/ui/Button';

export default function Header() {
  const { data: session } = useSession();

  return (
    <header className="h-16 border-b border-gray-200 bg-white">
      <div className="flex items-center justify-between h-full px-6">
        <div className="flex items-center gap-4">
          <Link href="/dashboard" className="text-xl font-bold text-gray-900">
            CodeReview AI
          </Link>
        </div>

        <div className="flex items-center gap-4">
          {session ? (
            <>
              <span className="text-sm text-gray-600">{session.user?.email}</span>
              <Button variant="outline" size="sm" onClick={() => signOut()}>
                Sign Out
              </Button>
            </>
          ) : (
            <Link href="/login">
              <Button variant="primary" size="sm">
                Sign In
              </Button>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
