'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { analysisApi } from '@/lib/api';
import { Card, CardContent, CardHeader } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Spinner } from '@/components/ui/Spinner';
import Button from '@/components/ui/Button';
import { formatScore, getGradeColor } from '@/lib/utils';
import type { Analysis } from '@/types';

export default function DashboardPage() {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAnalyses = async () => {
      try {
        const response = await analysisApi.list(1, 10);
        setAnalyses(response.data.items);
      } catch (error) {
        console.error('Failed to fetch analyses');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAnalyses();
  }, []);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600">Your recent code analyses</p>
          </div>
          <Link href="/analysis/new">
            <Button>New Analysis</Button>
          </Link>
        </div>

        {isLoading ? (
          <div className="flex justify-center py-12">
            <Spinner size="lg" />
          </div>
        ) : analyses.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-gray-500 mb-4">No analyses yet</p>
              <Link href="/analysis/new">
                <Button>Analyze Your First Code</Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {analyses.map((analysis) => (
              <Link key={analysis.id} href={`/analysis/${analysis.id}`}>
                <Card className="hover:shadow-md transition-shadow cursor-pointer">
                  <CardContent className="flex items-center justify-between p-4">
                    <div className="flex items-center gap-4">
                      <div>
                        <p className="font-medium text-gray-900">
                          {analysis.file_name || `${analysis.language} code`}
                        </p>
                        <p className="text-sm text-gray-500">
                          {new Date(analysis.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <Badge variant={
                        analysis.status === 'completed' ? 'success' :
                        analysis.status === 'failed' ? 'error' : 'warning'
                      }>
                        {analysis.status}
                      </Badge>
                      {analysis.overall_score !== null && (
                        <div className="text-right">
                          <span className={`text-2xl font-bold ${getGradeColor(analysis.grade || 'F')}`}>
                            {analysis.grade}
                          </span>
                          <p className="text-sm text-gray-500">
                            {formatScore(analysis.overall_score)}
                          </p>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
