'use client';

import { SimulationData } from '@/lib/types';
import { ResponsiveContainer, BarChart, Bar, CartesianGrid } from 'recharts';

interface VolumeChartProps {
  simulation?: SimulationData | null;
  isLoading?: boolean;
}

export function VolumeChart({ simulation, isLoading }: VolumeChartProps) {
  if (isLoading || !simulation) {
    return (
      <div className="brutalist-card bg-black p-4 flex items-center justify-center min-h-[80px]">
        <div className="font-mono text-[#CBF900] uppercase animate-pulse">Loading Volume...</div>
      </div>
    );
  }

  return (
    <div className="brutalist-card bg-black p-2 h-[80px] w-full flex items-center justify-between gap-4">
      <div className="-rotate-90 origin-center whitespace-nowrap min-w-[20px] px-1 font-sans font-bold text-xs uppercase text-[#CBF900] tracking-widest text-center mt-6">
        VOL
      </div>
      <div className="flex-grow h-full pt-1 pr-2">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={simulation.priceHistory} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="#222222" vertical={false} />
            <Bar dataKey="volume" fill="#CBF900" isAnimationActive={false} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
