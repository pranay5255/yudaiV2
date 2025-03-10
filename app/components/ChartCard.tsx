import ReactECharts from 'echarts-for-react';
import { EChartsOption } from 'echarts';

interface ChartCardProps {
  title: string;
  options: EChartsOption;
  onRemove: () => void;
}

export const ChartCard: React.FC<ChartCardProps> = ({ title, options, onRemove }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold">{title}</h2>
        <button 
          onClick={onRemove}
          className="text-red-500 hover:text-red-700"
        >
          Remove
        </button>
      </div>
      <ReactECharts option={options} style={{ height: '400px' }} />
    </div>
  );
}; 