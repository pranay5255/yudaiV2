'use client'

import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';

const formSchema = z.object({
  projectPrompt: z.string().min(1, 'Project prompt is required'),
  dataSource: z.string().min(1, 'Data source is required'),
  metrics: z.string().min(1, 'Desired metrics are required'),
});

type FormValues = z.infer<typeof formSchema>;

export default function DashboardGenPage() {
  const router = useRouter();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({ resolver: zodResolver(formSchema) });

  const onSubmit = (data: FormValues) => {
    const id = Date.now().toString();
    const config = JSON.stringify(data);
    router.push(`/preview/${id}?config=${encodeURIComponent(config)}`);
  };

  return (
    <div className="max-w-xl mx-auto py-10 space-y-6">
      <h1 className="text-2xl font-semibold">Generate Dashboard</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-2">
          <label className="block text-sm font-medium" htmlFor="projectPrompt">Project Prompt</label>
          <Input id="projectPrompt" {...register('projectPrompt')} />
          {errors.projectPrompt && (
            <p className="text-sm text-red-600">{errors.projectPrompt.message}</p>
          )}
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium" htmlFor="dataSource">Data Source</label>
          <Input id="dataSource" {...register('dataSource')} />
          {errors.dataSource && (
            <p className="text-sm text-red-600">{errors.dataSource.message}</p>
          )}
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium" htmlFor="metrics">Desired Metrics</label>
          <Textarea id="metrics" {...register('metrics')} />
          {errors.metrics && (
            <p className="text-sm text-red-600">{errors.metrics.message}</p>
          )}
        </div>
        <Button type="submit">Preview Dashboard</Button>
      </form>
    </div>
  );
}
