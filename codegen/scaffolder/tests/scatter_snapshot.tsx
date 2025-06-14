"use client";
// @ts-nocheck
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

interface DataPoint {
  a: number;
  b: number;
  c: string;
}

export default function ScatterChartComponent({ data }: { data: DataPoint[] }) {
  return (
    <ScatterChart width={400} height={300}>
      <CartesianGrid />
      <XAxis dataKey="a" type="number" />
      <YAxis dataKey="b" type="number" />
      <Tooltip />
      <Legend />
      <Scatter dataKey="b" name="MyScatter" data={data} />
    </ScatterChart>
  );
}
