import React from 'react';

interface SidebarProps {
  columnTypes: {
    datetime: string[];
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
              {columnMissingness[col] > 0 && (
                <span className="mr-2">Missing: {columnMissingness[col].toFixed(1)}%</span>
              )}
              <span>Unique: {columnCardinality[col]}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="w-64 bg-gray-800 border-r border-gray-700 p-4 overflow-y-auto">
      <h2 className="text-lg font-semibold text-white mb-6">Dataset Columns</h2>
      
      {columnTypes.datetime.length > 0 && 
        renderColumnGroup('Time-based', columnTypes.datetime)}
      
      {columnTypes.numeric.length > 0 && 
        renderColumnGroup('Numeric', columnTypes.numeric)}
      
      {columnTypes.categorical_low_cardinality.length > 0 && 
        renderColumnGroup('Categories', columnTypes.categorical_low_cardinality)}
      
      {columnTypes.categorical_high_cardinality.length > 0 && 
        renderColumnGroup('Text', columnTypes.categorical_high_cardinality)}
    </div>
  );
}; 