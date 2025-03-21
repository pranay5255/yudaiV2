'use client';

import { useDataset } from '../context/DatasetContext';
import { Sidebar } from '../components/Sidebar';
import { DataGraph } from '../components/DataGraph';
import { DataTable } from '../components/DataTable';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function DataGraphPage() {
    const { datasetStats } = useDataset();
    const router = useRouter();

    useEffect(() => {
        if (!datasetStats) {
            router.push('/');
        }
    }, [datasetStats, router]);

    if (!datasetStats) {
        return null;
    }

    return (
        <div className="min-h-screen bg-gray-900 flex">
            <Sidebar datasetStats={datasetStats} />
            <div className="flex-1 flex flex-col">
                {/* Header */}
                <div className="bg-gray-800 p-4 border-b border-gray-700">
                    <div className="max-w-7xl mx-auto">
                        <h1 className="text-2xl font-bold text-white">Data Graph</h1>
                    </div>
                </div>

                {/* Main content area */}
                <div className="flex-1 flex flex-col">
                    {/* Graph component - 25% height */}
                    <div className="h-1/3 w-full border-b border-gray-700">
                        <DataGraph />
                    </div>

                    {/* Table component - 75% height */}
                    <div className="flex-1 w-full">
                        <DataTable />
                    </div>
                </div>
            </div>
        </div>
    );
}
