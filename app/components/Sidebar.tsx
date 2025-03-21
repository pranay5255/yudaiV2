import React from 'react';
import { DatasetProfile } from '../../codegen/app/models';

interface SidebarProps {
    datasetStats: DatasetProfile;
}

export const Sidebar: React.FC<SidebarProps> = ({ datasetStats }) => {
    const renderColumns = () => {
        const columns = Object.entries(datasetStats.variables);
        const maxHeight = columns.length > 10 ? '500px' : 'auto';
        
        return (
            <div className="mb-4">
                <h3 className="text-gray-400 text-sm font-semibold mb-2 ">Columns</h3>
                <div 
                    className="space-y-1 overflow-y-auto" 
                    style={{ maxHeight }}
                >
                    {columns.map(([col, stats]) => (
                        <div
                            key={col}
                            className="p-2 rounded hover:bg-gray-700 cursor-pointer"
                        >
                            <div className="flex justify-between items-center">
                                <div className="flex flex-col">
                                    <span className="text-blue-400">{col}</span>
                                    <span className="text-xs text-gray-400">
                                        Distinct values: {stats.n_distinct}
                                    </span>
                                </div>
                                <button 
                                    onClick={() => navigator.clipboard.writeText(col)}
                                    className="text-gray-400 hover:text-white text-xs px-4 py-1 rounded bg-gray-600 hover:bg-gray-500"
                                >
                                    Copy
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        );
    };

    return (
        <div className="w-72 bg-gray-800 border-r border-gray-700 p-4 ">
            {/* Dataset Overview - Only essential metrics */}
            <div className="mb-6">
                <h2 className="text-lg font-semibold text-white">Dataset Summary</h2>
                <div className="mt-2 text-sm text-gray-400">
                    <div>Rows: {datasetStats.table.n.toLocaleString()}</div>
                    <div>Columns: {datasetStats.table.n_var}</div>
                    <div className="text-yellow-500">
                        Missing: {(datasetStats.table.p_cells_missing * 100).toFixed(1)}%
                    </div>
                    <div className="text-yellow-500">
                        Duplicates: {datasetStats.table.n_duplicates}
                    </div>
                </div>
            </div>

            {/* All Columns */}
            {renderColumns()}

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