'use client';

import React, { createContext, useContext, useState } from 'react';
import { DatasetProfile } from '../../codegen/app/models';

interface DatasetContextType {
    datasetStats: DatasetProfile | null;
    setDatasetStats: (stats: DatasetProfile | null) => void;
}

const DatasetContext = createContext<DatasetContextType | undefined>(undefined);

export function DatasetProvider({ children }: { children: React.ReactNode }) {
    const [datasetStats, setDatasetStats] = useState<DatasetProfile | null>(null);

    return (
        <DatasetContext.Provider value={{ datasetStats, setDatasetStats }}>
            {children}
        </DatasetContext.Provider>
    );
}

export function useDataset() {
    const context = useContext(DatasetContext);
    if (context === undefined) {
        throw new Error('useDataset must be used within a DatasetProvider');
    }
    return context;
} 