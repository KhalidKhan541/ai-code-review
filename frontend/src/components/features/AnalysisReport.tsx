'use client';

import { cn, formatScore, getGradeColor } from '@/lib/utils';
import { ScoreCard } from '@/components/ui/ScoreCard';
import type { AnalysisDetail } from '@/types';

interface AnalysisReportProps {
  analysis: AnalysisDetail;
}

export default function AnalysisReport({ analysis }: AnalysisReportProps) {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <div className={cn('text-6xl font-bold', getGradeColor(analysis.grade || 'F'))}>
          {analysis.grade}
        </div>
        <div className="text-3xl font-semibold text-gray-700 mt-2">
          {formatScore(analysis.overall_score || 0)} / 100
        </div>
        <p className="text-gray-500 mt-2">{analysis.report?.summary}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <ScoreCard label="Test Coverage" score={analysis.scores?.test_coverage || 0} />
        <ScoreCard label="Dependency Health" score={analysis.scores?.dependency_health || 0} />
        <ScoreCard label="Code Cleanliness" score={analysis.scores?.code_cleanliness || 0} />
        <ScoreCard label="Architecture" score={analysis.scores?.architecture || 0} />
        <ScoreCard label="Security" score={analysis.scores?.security || 0} />
      </div>

      {analysis.issues.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Issues Found ({analysis.issues.length})
          </h3>
          <div className="space-y-3">
            {analysis.issues.map((issue) => (
              <div
                key={issue.id}
                className={cn(
                  'p-4 rounded-lg border',
                  issue.severity === 'critical' && 'border-red-200 bg-red-50',
                  issue.severity === 'high' && 'border-orange-200 bg-orange-50',
                  issue.severity === 'medium' && 'border-yellow-200 bg-yellow-50',
                  issue.severity === 'low' && 'border-green-200 bg-green-50'
                )}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-xs font-medium uppercase text-gray-500">
                      {issue.category}
                    </span>
                    {issue.line_number && (
                      <span className="ml-2 text-xs text-gray-400">
                        Line {issue.line_number}
                      </span>
                    )}
                  </div>
                  <span
                    className={cn(
                      'px-2 py-1 text-xs font-medium rounded',
                      issue.severity === 'critical' && 'bg-red-100 text-red-800',
                      issue.severity === 'high' && 'bg-orange-100 text-orange-800',
                      issue.severity === 'medium' && 'bg-yellow-100 text-yellow-800',
                      issue.severity === 'low' && 'bg-green-100 text-green-800'
                    )}
                  >
                    {issue.severity}
                  </span>
                </div>
                <p className="mt-2 text-sm text-gray-700">{issue.message}</p>
                {issue.suggestion && (
                  <p className="mt-1 text-sm text-gray-600 italic">
                    Suggestion: {issue.suggestion}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {analysis.report?.recommendations && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommendations</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(analysis.report.recommendations).map(([key, value]) => (
              <div key={key} className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-medium text-gray-900 capitalize">
                  {key.replace(/_/g, ' ')}
                </h4>
                <p className="text-sm text-gray-600 mt-1">{value}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
