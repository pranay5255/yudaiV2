interface ChartType {
  id: string;
  name: string;
  type: 'line' | 'bar' | 'pie';
}

interface ChartSelectorProps {
  availableCharts: ChartType[];
  onAddChart: (chartId: string) => void;
}

export const ChartSelector: React.FC<ChartSelectorProps> = ({ availableCharts, onAddChart }) => {
  return (
    <div className="mb-6">
      <h2 className="text-lg font-semibold mb-2">Add Visualization</h2>
      <div className="flex gap-2">
        {availableCharts.map((chart) => (
          <button
            key={chart.id}
            onClick={() => onAddChart(chart.id)}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Add {chart.name}
          </button>
        ))}
      </div>
    </div>
  );
}; 