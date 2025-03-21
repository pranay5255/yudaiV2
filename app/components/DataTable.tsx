import React from 'react';

interface DataTableProps {
    // In a real app, this would be properly typed based on your data structure
    data?: any[][];
    columns?: string[];
}

export const DataTable: React.FC<DataTableProps> = ({ 
    data = [
        [1, 'John', 'Doe', 'john@example.com', 'Active'],
        [2, 'Jane', 'Smith', 'jane@example.com', 'Inactive'],
        [3, 'Bob', 'Johnson', 'bob@example.com', 'Active'],
        [4, 'Alice', 'Brown', 'alice@example.com', 'Active'],
        [5, 'Charlie', 'Davis', 'charlie@example.com', 'Inactive']
    ],
    columns = ['ID', 'First Name', 'Last Name', 'Email', 'Status']
}) => {
    return (
        <div className="w-full h-full p-4 overflow-hidden">
            <div className="overflow-x-auto">
                <table className="min-w-full bg-gray-800 text-white">
                    <thead>
                        <tr>
                            {columns.map((column, index) => (
                                <th
                                    key={index}
                                    className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider whitespace-nowrap"
                                >
                                    {column}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="bg-gray-700 divide-y divide-gray-600">
                        {data.map((row, rowIndex) => (
                            <tr key={rowIndex}>
                                {row.map((cell, cellIndex) => (
                                    <td
                                        key={cellIndex}
                                        className="px-6 py-4 whitespace-nowrap text-sm text-gray-300"
                                    >
                                        {cell}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}; 