import Link from 'next/link';
import Button from '@/components/ui/Button';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-primary-50 to-white">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center max-w-3xl mx-auto">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            AI-Powered Code Reviews
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Get instant, detailed code analysis with security checks, performance insights,
            and improvement suggestions powered by advanced AI.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/register">
              <Button size="lg">Get Started Free</Button>
            </Link>
            <Link href="/login">
              <Button variant="outline" size="lg">Sign In</Button>
            </Link>
          </div>
        </div>

        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <div className="text-3xl mb-4">🔒</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Security Analysis</h3>
            <p className="text-gray-600">Detect vulnerabilities, SQL injections, and security issues before they reach production.</p>
          </div>
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <div className="text-3xl mb-4">⚡</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Performance Insights</h3>
            <p className="text-gray-600">Identify bottlenecks, memory leaks, and optimization opportunities.</p>
          </div>
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <div className="text-3xl mb-4">📊</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Code Quality Scores</h3>
            <p className="text-gray-600">Get comprehensive scores and grades for your code quality metrics.</p>
          </div>
        </div>
      </div>
    </main>
  );
}
