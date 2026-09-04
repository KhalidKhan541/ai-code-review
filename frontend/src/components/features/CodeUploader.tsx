'use client';

import { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { toast } from 'react-hot-toast';
import { analysisApi } from '@/lib/api';
import { analysisSchema, type AnalysisInput } from '@/lib/validations';
import { SUPPORTED_LANGUAGES } from '@/lib/utils';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { Card, CardContent } from '@/components/ui/Card';

export default function CodeUploader() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [codeContent, setCodeContent] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<AnalysisInput>({
    resolver: zodResolver(analysisSchema),
  });

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target?.result as string;
        setCodeContent(content);
        setValue('code_content', content);
        setValue('file_name', file.name);

        const ext = file.name.split('.').pop()?.toLowerCase();
        const langMap: Record<string, string> = {
          py: 'python',
          js: 'javascript',
          ts: 'typescript',
          java: 'java',
          go: 'go',
          rs: 'rust',
          cpp: 'cpp',
          cs: 'csharp',
        };
        if (ext && langMap[ext]) {
          setValue('language', langMap[ext]);
        }
      };
      reader.readAsText(file);
    }
  };

  const onSubmit = async (data: AnalysisInput) => {
    setIsLoading(true);
    try {
      const response = await analysisApi.create({
        code_content: data.code_content,
        language: data.language,
        file_name: data.file_name,
      });
      toast.success('Analysis started!');
      router.push(`/analysis/${response.data.id}`);
    } catch (error) {
      toast.error('Failed to start analysis');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardContent className="p-6">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload Code File
            </label>
            <div
              className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-500 transition-colors cursor-pointer"
              onClick={() => fileInputRef.current?.click()}
            >
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p className="mt-2 text-sm text-gray-600">Click to upload or drag and drop</p>
              <p className="mt-1 text-xs text-gray-500">Supports Python, JavaScript, TypeScript, and more</p>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              accept=".py,.js,.ts,.java,.go,.rs,.cpp,.cs"
              onChange={handleFileUpload}
            />
          </div>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">or paste code</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Code Content
            </label>
            <textarea
              className="w-full h-64 p-4 font-mono text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="Paste your code here..."
              value={codeContent}
              onChange={(e) => {
                setCodeContent(e.target.value);
                setValue('code_content', e.target.value);
              }}
            />
            {errors.code_content && (
              <p className="mt-1 text-sm text-red-600">{errors.code_content.message}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Programming Language
              </label>
              <select
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                {...register('language')}
              >
                <option value="">Select language</option>
                {SUPPORTED_LANGUAGES.map((lang) => (
                  <option key={lang.value} value={lang.value}>
                    {lang.label}
                  </option>
                ))}
              </select>
              {errors.language && (
                <p className="mt-1 text-sm text-red-600">{errors.language.message}</p>
              )}
            </div>

            <Input
              label="File Name (optional)"
              placeholder="example.py"
              {...register('file_name')}
            />
          </div>

          <Button type="submit" isLoading={isLoading} className="w-full" size="lg">
            Analyze Code
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
