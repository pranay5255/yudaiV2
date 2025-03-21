import React from 'react';
import ReactECharts from 'echarts-for-react';

interface DataNode {
    name: string;
    value: string;
}

interface DataLink {
    source: string;
    target: string;
    label: string;
}

export const DataGraph: React.FC = () => {
    // Sample data - in a real app, this would come from props or an API
    const nodes: DataNode[] = [
        { name: 'Original', value: 'v1' },
        { name: 'Cleaned', value: 'v2' },
        { name: 'Transformed', value: 'v3' }
    ];

    const links: DataLink[] = [
        { source: 'Original', target: 'Cleaned', label: 'Remove duplicates' },
        { source: 'Cleaned', target: 'Transformed', label: 'Normalize values' }
    ];

    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c}'
        },
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [{
            type: 'graph',
            layout: 'circular',
            symbolSize: 50,
            roam: true,
            label: {
                show: true,
                position: 'right',
                formatter: '{b}'
            },
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 10],
            edgeLabel: {
                fontSize: 12,
                show: true,
                formatter: '{c}'
            },
            data: nodes.map(node => ({
                name: node.name,
                value: node.value,
                itemStyle: {
                    color: '#1890ff'
                }
            })),
            links: links.map(link => ({
                source: link.source,
                target: link.target,
                name: link.label,
                value: link.label,
                lineStyle: {
                    color: '#999',
                    width: 2
                }
            })),
            lineStyle: {
                color: '#999',
                width: 2,
                curveness: 0.3
            }
        }]
    };

    return (
        <div className="w-full h-full p-4">
            <ReactECharts 
                option={option}
                style={{ height: '100%', width: '100%' }}
            />
        </div>
    );
}; 