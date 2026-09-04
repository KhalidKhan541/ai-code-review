import { cn } from '@/lib/utils';

interface ScoreCardProps {
  label: string;
  score: number;
  maxScore?: number;
  className?: string;
}

function getScoreColor(score: number): string {
  if (score >= 90) return 'text-green-600';
  if (score >= 70) return 'text-blue-600';
  if (score >= 50) return 'text-yellow-600';
  return 'text-red-600';
}

function getProgressColor(score: number): string {
  if (score >= 90) return 'bg-green-500';
  if (score >= 70) return 'bg-blue-500';
  if (score >= 50) return 'bg-yellow-500';
  return 'bg-red-500';
}

export function ScoreCard({ label, score, maxScore = 100, className }: ScoreCardProps) {
  const percentage = (score / maxScore) * 100;

  return (
    <div className={cn('rounded-lg border border-gray-200 p-4', className)}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-600">{label}</span>
        <span className={cn('text-2xl font-bold', getScoreColor(score))}>{score}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={cn('h-2 rounded-full transition-all duration-500', getProgressColor(score))}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
