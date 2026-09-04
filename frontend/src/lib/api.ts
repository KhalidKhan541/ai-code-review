import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import type { ApiError } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ApiError>) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    api.post('/auth/register', data),
  refreshToken: (token: string) =>
    api.post('/auth/refresh', {}, { headers: { Authorization: `Bearer ${token}` } }),
  getMe: () => api.get('/auth/me'),
};

export const analysisApi = {
  create: (data: { code_content: string; language: string; file_name?: string }) =>
    api.post('/analysis/', data),
  list: (page = 1, perPage = 10) =>
    api.get('/analysis/', { params: { page, per_page: perPage } }),
  get: (id: string) => api.get(`/analysis/${id}`),
};

export const reportsApi = {
  get: (analysisId: string) => api.get(`/reports/${analysisId}`),
  getIssues: (analysisId: string) => api.get(`/reports/${analysisId}/issues`),
};
