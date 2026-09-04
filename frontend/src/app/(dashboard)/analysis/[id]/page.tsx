'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import DashboardLayout from '@/components/layout/DashboardLayout';
import AnalysisReport from '@/components/features/AnalysisReport';
import { analysisApi } from '@/lib/api';
import { Spinner } from '@/components/ui/Spinner';
import { Alert } from '@/components/ui/Alert';
import type { AnalysisDetail } from '@/types';

export default function AnalysisDetailPage() {
  const params = useParams();
  const [analysis, setAnalysis] = useState<AnalysisDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await analysisApi.get(params.id as string);
        setAnalysis(response.data);
      } catch (err) {
        setError('Failed to load analysis');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAnalysis();
  }, [params.id]);

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      </DashboardLayout>
    );
  }

  if (error || !analysis) {
    return (
      <DashboardLayout>
        <Alert variant="error" title="Error">
          {error || 'Analysis not found'}
        </Alert>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <AnalysisReport analysis={analysis} />
    </DashboardLayout>
  );
}
