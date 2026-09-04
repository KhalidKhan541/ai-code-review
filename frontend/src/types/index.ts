export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string | null;
  avatar_url: string | null;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Analysis {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  language: string;
  file_name: string | null;
  overall_score: number | null;
  grade: string | null;
  scores: AnalysisScores | null;
  created_at: string;
}

export interface AnalysisScores {
  test_coverage: number;
  dependency_health: number;
  code_cleanliness: number;
  architecture: number;
  security: number;
}

export interface AnalysisDetail extends Analysis {
  code_content: string;
  metadata_: Record<string, unknown> | null;
  report: Report | null;
  issues: Issue[];
}

export interface Report {
  id: string;
  summary: string;
  recommendations: Record<string, string> | null;
  detailed_scores: Record<string, unknown> | null;
  created_at: string;
}

export interface Issue {
  id: string;
  category: 'security' | 'performance' | 'quality' | 'architecture';
  severity: 'critical' | 'high' | 'medium' | 'low';
  line_number: number | null;
  column: number | null;
  message: string;
  suggestion: string | null;
  rule_id: string | null;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
}

export interface ApiError {
  detail: string;
}
