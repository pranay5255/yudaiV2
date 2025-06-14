'use client'

import { useSearchParams, useParams } from 'next/navigation';
import React from 'react';
import { Button } from '@/components/ui/button';
import toast from 'react-hot-toast';

export default function PreviewPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const config = searchParams.get('config');
  const id = params.id as string;

  const handleDownload = async () => {
    try {
      const res = await fetch(`/api/export?id=${id}`);
      if (!res.ok) throw new Error('Failed to download');
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `dashboard_${id}.zip`;
      a.click();
      toast.success('Download started');
    } catch {
      toast.error('Failed to download');
    }
  };

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">Preview Dashboard {id}</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="h-40 bg-gray-200 rounded" />
        <div className="h-40 bg-gray-200 rounded" />
        <div className="h-40 bg-gray-200 rounded" />
        <div className="h-40 bg-gray-200 rounded" />
      </div>
      <Button onClick={handleDownload}>Download Zip</Button>
      <pre className="whitespace-pre-wrap text-sm bg-gray-100 p-2 rounded">
        {config}
      </pre>
    </div>
  );
}
