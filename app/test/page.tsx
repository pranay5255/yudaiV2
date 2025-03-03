'use client';

import { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { parse } from 'csv-parse/sync';

interface SampleData {
  order_id: string;
  customer_id: string;
  order_date: string;
  product_category: string;
  price: number;
  quantity: number;
  total_amount: number;
  status: string;
  payment_method: string;
}

export default function Dashboard() {
  const [data, setData] = useState<SampleData[]>([]);

  useEffect(() => {
    // In a real application, you would fetch this data from an API
    fetch('/api/sample-data')
      .then((res) => res.text())
      .then((csvData) => {
        const parsedData = parse(csvData, {
          columns: true,
          skip_empty_lines: true,
        });
        setData(parsedData);
      });
  }, []);

  // Chart 1: Sales Trends Over Time
  const getSalesTrendsOptions = () => {
    const chartData = data.map((item) => ({
      date: item.order_date,
      value: parseFloat(item.total_amount.toString()),
    }));

    return {
      title: { text: 'Sales Trends Over Time' },
      tooltip: { trigger: 'axis' },
      xAxis: { 
        type: 'category',
        data: chartData.map(d => d.date)
      },
      yAxis: { type: 'value' },
      series: [{
        type: 'line',
        data: chartData.map(d => d.value),
        smooth: true,
        areaStyle: {},
      }]
    };
  };

  // Chart 2: Sales by Product Category
  const getProductCategoryOptions = () => {
    const categoryData = data.reduce((acc, item) => {
      acc[item.product_category] = (acc[item.product_category] || 0) + parseFloat(item.total_amount.toString());
      return acc;
    }, {} as Record<string, number>);

    const chartData = Object.entries(categoryData).map(([category, value]) => ({
      category,
      value: value.toString(),
    }));

    return {
      title: { text: 'Sales by Product Category' },
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: chartData.map(d => d.category),
      },
      yAxis: { type: 'value' },
      series: [{
        type: 'bar',
        data: chartData.map(d => parseFloat(d.value)),
      }]
    };
  };

  // Chart 3: Payment Methods Distribution
  const getPaymentMethodOptions = () => {
    const paymentData = data.reduce((acc, item) => {
      acc[item.payment_method] = (acc[item.payment_method] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const chartData = Object.entries(paymentData).map(([name, value]) => ({
      name,
      value,
    }));

    return {
      title: { text: 'Payment Methods Distribution' },
      tooltip: { trigger: 'item' },
      legend: { orient: 'vertical', right: 'right' },
      series: [{
        type: 'pie',
        radius: '50%',
        data: chartData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    };
  };

  // Chart 4: Order Status Breakdown
  const getOrderStatusOptions = () => {
    const statusData = data.reduce((acc, item) => {
      acc[item.status] = (acc[item.status] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const chartData = Object.entries(statusData).map(([name, value]) => ({
      name,
      value,
    }));

    return {
      title: { text: 'Order Status Breakdown' },
      tooltip: { trigger: 'item' },
      legend: { orient: 'vertical', left: 'right' },
      series: [{
        type: 'pie',
        radius: '50%',
        data: chartData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    };
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Sales Dashboard</h1>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <ReactECharts option={getSalesTrendsOptions()} style={{ height: '400px' }} />
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <ReactECharts option={getProductCategoryOptions()} style={{ height: '400px' }} />
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <ReactECharts option={getPaymentMethodOptions()} style={{ height: '400px' }} />
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <ReactECharts option={getOrderStatusOptions()} style={{ height: '400px' }} />
        </div>
      </div>
    </div>
  );
}
