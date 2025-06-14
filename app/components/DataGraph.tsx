import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { useDataset } from '../context/DatasetContext';

interface DataNode {
    name: string;
    value: string;
    version: string;
}

interface DataLink {
    source: string;
    target: string;
    label: string;
    transformation: string;
}


export const DataGraph: React.FC = () => {
    const { datasetStats } = useDataset();
    const [nodes, setNodes] = useState<DataNode[]>([
        { name: 'Original Data', value: 'v0.0', version: 'v0.0' }
    ]);
    const [links, setLinks] = useState<DataLink[]>([]);

    // Effect to handle transformation updates
    useEffect(() => {
        if (datasetStats?.transformations) {
            const initialNodes: DataNode[] = [
                { name: 'Original Data', value: 'v0.0', version: 'v0.0' }
            ];
            const initialLinks: DataLink[] = [];

            datasetStats.transformations.forEach((transformation, index) => {
                const version = `v${index + 1}.0`;
                const newNode: DataNode = {
                    name: `Version ${version}`,
                    value: version,
                    version
                };
                const prevVersion = initialNodes[index].version;
                const newLink: DataLink = {
                    source: prevVersion,
                    target: version,
                    label: transformation.description,
                    transformation: transformation.description
                };
                initialNodes.push(newNode);
                initialLinks.push(newLink);
            });

            setNodes(initialNodes);
            setLinks(initialLinks);
        }
    }, [datasetStats?.transformations]);

    const option = {
        tooltip: {
            trigger: 'item',
            formatter: (params: { dataType: string; data: { name: string; version?: string; transformation?: string } }) => {
                if (params.dataType === 'node') {
                    return `${params.data.name}<br/>Version: ${params.data.version}`;
                }
                return `Transformation: ${params.data.transformation}`;
            }
        },
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [{
            type: 'graph',
            layout: 'force',
            force: {
                repulsion: 100,
                edgeLength: 100
            },
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
                version: node.version,
                itemStyle: {
                    color: '#1890ff'
                }
            })),
            links: links.map(link => ({
                source: link.source,
                target: link.target,
                name: link.label,
                transformation: link.transformation,
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