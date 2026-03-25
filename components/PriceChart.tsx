'use client';

import { SimulationData, PricePoint } from '@/lib/types';
import {
  ResponsiveContainer,
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';

interface PriceChartProps {
  simulation?: SimulationData | null;
  isLoading?: boolean;
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="brutalist-card bg-black border-[#CBF900] p-3 shadow-[4px_4px_0px_rgba(203,249,0,0.5)]">
        <p className="font-mono text-xs font-bold text-white mb-2">{label}</p>
        {payload.map((entry: any, index: number) => (
          <p key={index} className="font-mono text-sm font-bold uppercase" style={{ color: entry.color }}>
            {entry.name}: ${entry.value.toFixed(2)}
          </p>
        ))}
      </div>
    );
  }
  return null;
}

export function PriceChart({ simulation, isLoading }: PriceChartProps) {
  if (isLoading || !simulation) {
    return (
      <div className="brutalist-card bg-black p-6 flex items-center justify-center min-h-[300px]">
        <div className="font-mono text-white/50 uppercase">Loading Data...</div>
      </div>
    );
  }

  return (
    <div className="brutalist-card bg-black p-4 w-full h-[350px]">
      <div className="font-mono text-sm font-bold text-white uppercase mb-4 tracking-widest flex items-center gap-2">
        <span className="w-2 h-2 bg-[#CBF900]" /> Base Prediction Matrix
      </div>
      <ResponsiveContainer width="100%" height="85%">
        <ComposedChart data={simulation.priceHistory} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="colorSimulated" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#CBF900" stopOpacity={0.2} />
              <stop offset="95%" stopColor="#CBF900" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="#222222" vertical={false} />
          <XAxis
            dataKey="time"
            stroke="#666666"
            fontSize={10}
            fontFamily="var(--font-silkscreen), monospace"
            tickMargin={10}
          />
          <YAxis
            stroke="#666666"
            fontSize={10}
            fontFamily="var(--font-silkscreen), monospace"
            domain={['auto', 'auto']}
          />
          <Tooltip content={<CustomTooltip />} />
          
          <Line
            type="monotone"
            dataKey="historical"
            name="Historical"
            stroke="#FFFFFF"
            strokeWidth={2}
            dot={{ r: 2, fill: '#FFFFFF' }}
            activeDot={{ r: 4 }}
            isAnimationActive={true}
          />
          
          <Area
            type="monotone"
            dataKey="simulated"
            name="Simulated"
            stroke="#CBF900"
            strokeWidth={2}
            strokeDasharray="5 5"
            fillOpacity={1}
            fill="url(#colorSimulated)"
            isAnimationActive={false}
          />
          
          <Line
            type="monotone"
            dataKey="bull"
            name="Bull Scenario"
            stroke="#A56DFC"
            strokeWidth={2}
            strokeDasharray="2 4"
            dot={false}
            isAnimationActive={false}
          />
          
          <Line
            type="monotone"
            dataKey="bear"
            name="Bear Scenario"
            stroke="#E87BE9"
            strokeWidth={2}
            strokeDasharray="2 4"
            dot={false}
            isAnimationActive={false}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
