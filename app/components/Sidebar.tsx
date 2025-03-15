import React from 'react';
import { DatasetProfile } from '../../codegen/app/models';

interface SidebarProps {
    datasetStats: DatasetProfile;
}

export const Sidebar: React.FC<SidebarProps> = ({ datasetStats }) => {
    const renderColumnGroup = (title: string, columns: string[]) => (
        <div className="mb-4">
            <h3 className="text-gray-400 text-sm font-semibold mb-2">{title}</h3>
            <div className="space-y-1">
                {columns.map((col) => {
                    const stats = datasetStats.variables[col];
                    const hasWarnings = stats.p_missing > 0 || stats.n_distinct === 1;
                    
                    return (
                        <div
                            key={col}
                            className={`p-2 rounded hover:bg-gray-700 cursor-pointer ${
                                hasWarnings ? 'border-l-2 border-yellow-500' : ''
                            }`}
                        >
                            <div className="flex justify-between items-center">
                                <span className="text-white">{col}</span>
                                {stats.is_unique && (
                                    <span className="text-xs text-blue-400">unique</span>
                                )}
                            </div>
                            {hasWarnings && (
                                <div className="text-xs text-gray-500 mt-1">
                                    {stats.p_missing > 0 && (
                                        <span className="text-yellow-500">
                                            Missing: {(stats.p_missing * 100).toFixed(1)}%
                                        </span>
                                    )}
                                    {stats.n_distinct === 1 && (
                                        <span className="text-yellow-500">Constant</span>
                                    )}
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );

    // Group columns by their types
    const columnsByType = {
        datetime: Object.entries(datasetStats.variables)
            .filter(([, stats]) => stats.type === 'DateTime')
            .map(([name]) => name),
        numeric: Object.entries(datasetStats.variables)
            .filter(([, stats]) => stats.type === 'Numeric')
            .map(([name]) => name),
        categorical: Object.entries(datasetStats.variables)
            .filter(([, stats]) => stats.type === 'Categorical')
            .map(([name]) => name),
        text: Object.entries(datasetStats.variables)
            .filter(([, stats]) => stats.type === 'Text')
            .map(([name]) => name),
    };

    return (
        <div className="w-72 bg-gray-800 border-r border-gray-700 p-4 overflow-y-auto">
            {/* Dataset Overview - Only essential metrics */}
            <div className="mb-6">
                <h2 className="text-lg font-semibold text-white">Dataset Summary</h2>
                <div className="mt-2 text-sm text-gray-400">
                    <div>Rows: {datasetStats.table.n.toLocaleString()}</div>
                    <div>Columns: {datasetStats.table.n_var}</div>
                    {datasetStats.table.p_cells_missing > 0 && (
                        <div className="text-yellow-500">
                            Missing: {(datasetStats.table.p_cells_missing * 100).toFixed(1)}%
                        </div>
                    )}
                    {datasetStats.table.n_duplicates > 0 && (
                        <div className="text-yellow-500">
                            Duplicates: {datasetStats.table.n_duplicates}
                        </div>
                    )}
                </div>
            </div>

            {/* Column Groups - Only show if they have columns */}
            <div className="space-y-2">
                {columnsByType.datetime.length > 0 && 
                    renderColumnGroup('Time Columns', columnsByType.datetime)}
                
                {columnsByType.numeric.length > 0 && 
                    renderColumnGroup('Numeric', columnsByType.numeric)}
                
                {columnsByType.categorical.length > 0 && 
                    renderColumnGroup('Categories', columnsByType.categorical)}
                
                {columnsByType.text.length > 0 && 
                    renderColumnGroup('Text', columnsByType.text)}
            </div>

            {/* Alerts Section - If there are any */}
            {datasetStats.alerts.length > 0 && (
                <div className="mt-6 pt-4 border-t border-gray-700">
                    <h3 className="text-yellow-500 text-sm font-semibold mb-2">Warnings</h3>
                    <ul className="text-xs text-gray-400">
                        {datasetStats.alerts.slice(0, 3).map((alert, idx) => (
                            <li key={idx} className="mb-1">• {alert}</li>
                        ))}
                        {datasetStats.alerts.length > 3 && (
                            <li className="text-gray-500">
                                +{datasetStats.alerts.length - 3} more warnings
                            </li>
                        )}
                    </ul>
                </div>
            )}
        </div>
    );
}; 