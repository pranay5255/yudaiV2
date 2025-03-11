import React, { useEffect, useState } from 'react';

interface SidebarProps {
  columnTypes: {
    numeric: string[];
    categorical_low_cardinality: string[];
    categorical_high_cardinality: string[];
  };
  columnMissingness: Record<string, number>;
  columnCardinality: Record<string, number>;
}

export const Sidebar: React.FC<SidebarProps> = ({
  columnTypes,
  columnMissingness,
  columnCardinality,
}) => {
  const [columnData, setColumnData] = useState<SidebarProps>({
    columnTypes: {
      numeric: [],
      categorical_low_cardinality: [],
      categorical_high_cardinality: []
    },
    columnMissingness: {},
    columnCardinality: {}
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setColumnData({
      columnTypes,
      columnMissingness,
      columnCardinality
    });
  }, [columnTypes, columnMissingness, columnCardinality]);

  const renderColumnGroup = (title: string, columns: string[]) => (
    <div className="mb-6">
      <h3 className="text-gray-400 text-sm font-semibold mb-2">{title}</h3>
      <div className="space-y-1">
        {columns.map((col) => (
          <div
            key={col}
            className="p-2 rounded hover:bg-gray-700 cursor-pointer group"
          >
            <div className="text-gray-300 group-hover:text-white">{col}</div>
            <div className="text-xs text-gray-500">
              {columnData.columnMissingness[col] > 0 && (
                <span className="mr-2">
                  Missing: {columnData.columnMissingness[col].toFixed(1)}%
                </span>
              )}
              {columnData.columnCardinality[col] && (
                <span>Unique: {columnData.columnCardinality[col]}</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  if (error) {
    return (
      <div className="w-64 bg-gray-800 border-r border-gray-700 p-4">
        <div className="text-red-400">{error}</div>
      </div>
    );
  }

  return (
    <div className="w-64 bg-gray-800 border-r border-gray-700 p-4 overflow-y-auto">
      <h2 className="text-lg font-semibold text-white mb-6">
        Dataset Columns
      </h2>
      
      
      {columnData.columnTypes.numeric.length > 0 && 
        renderColumnGroup('Numeric', columnData.columnTypes.numeric)}
      
      {columnData.columnTypes.categorical_low_cardinality.length > 0 && 
        renderColumnGroup('Categories', columnData.columnTypes.categorical_low_cardinality)}
      
    </div>
  );
};