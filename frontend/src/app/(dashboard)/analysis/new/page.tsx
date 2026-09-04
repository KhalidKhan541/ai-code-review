'use client';

import DashboardLayout from '@/components/layout/DashboardLayout';
import CodeUploader from '@/components/features/CodeUploader';

export default function NewAnalysisPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">New Code Analysis</h1>
          <p className="text-gray-600">Upload or paste your code for AI-powered analysis</p>
        </div>
        <CodeUploader />
      </div>
    </DashboardLayout>
  );
}
