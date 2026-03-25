'use client';

import { SimulationData } from '@/lib/types';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line } from 'recharts';

interface AgentSwarmStatusProps {
  simulation?: SimulationData | null;
}

const COLORS = {
  bullish: '#CBF900',  // Lime
  neutral: '#A56DFC',  // Purple
  bearish: '#E87BE9',  // Pink
};

export function AgentSwarmStatus({ simulation }: AgentSwarmStatusProps) {
  if (!simulation) {
    return (
      <div className="brutalist-card bg-black p-5 flex items-center justify-center min-h-[300px]">
        <div className="font-mono text-[#A56DFC] uppercase animate-pulse">Waiting for Swarm...</div>
      </div>
    );
  }

  const { bullish, neutral, bearish } = simulation.sentiment;
  const total = bullish + neutral + bearish;

  const data = [
    { name: 'Bullish', value: bullish },
    { name: 'Neutral', value: neutral },
    { name: 'Bearish', value: bearish },
  ];

  // Dummy sentiment shift data for sparkline
  const sparklineData = Array.from({ length: 10 }).map((_, i) => ({
    name: i,
    val: Math.random() * 100,
  }));

  // Find dominant
  let dominant = 'NEUTRAL';
  let domScore = neutral;
  if (bullish > domScore) { dominant = 'BULLISH'; domScore = bullish; }
  if (bearish > domScore) { dominant = 'BEARISH'; domScore = bearish; }

  return (
    <div className="brutalist-card bg-white p-5 flex flex-col gap-5 relative">
      <div className="sticker-badge bg-[#E87BE9] text-black px-4 py-1.5 -rotate-2 w-max shadow-[3px_3px_0px_#000000] -ml-2 -mt-2">
        AGENT SWARM STATUS
      </div>

      <div className="flex flex-col items-center justify-center text-center mt-2">
        <span className="font-mono text-sm font-bold text-black uppercase mb-1">Total Active Agents</span>
        <motion.div
          key={simulation.totalAgents}
          initial={{ scale: 1.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="font-mono text-5xl font-bold tracking-tighter"
        >
          {simulation.totalAgents.toLocaleString()}
        </motion.div>
      </div>

      <div className="flex items-center gap-4">
        {/* Recharts PieChart */}
        <div className="w-[120px] h-[120px] relative shrink-0">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={35}
                outerRadius={55}
                stroke="#000000"
                strokeWidth={3}
                dataKey="value"
                isAnimationActive={true}
                animationDuration={800}
              >
                {data.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={entry.name === 'Bullish' ? COLORS.bullish : entry.name === 'Bearish' ? COLORS.bearish : COLORS.neutral}
                  />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          {/* Center Label */}
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <span className="font-sans font-[800] text-sm text-black -mt-1">{dominant}</span>
          </div>
        </div>

        {/* Legend */}
        <div className="flex flex-col gap-2 flex-grow">
          {data.map((item) => (
            <div key={item.name} className="flex justify-between items-center w-full">
              <div className="flex items-center gap-2">
                <div
                  className="w-3 h-3 border-2 border-black"
                  style={{
                    backgroundColor: item.name === 'Bullish' ? COLORS.bullish : item.name === 'Bearish' ? COLORS.bearish : COLORS.neutral,
                  }}
                />
                <span className="font-mono text-xs font-bold uppercase">{item.name}</span>
              </div>
              <span className="font-mono text-xs font-bold">
                {((item.value / total) * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Sparkline */}
      <div className="mt-2">
        <span className="font-mono text-xs font-bold text-black uppercase mb-1 block">Sentiment Shift</span>
        <div className="brutalist-card bg-black border-[3px] border-black shadow-[2px_2px_0px_#000000] w-full h-[40px] p-1">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={sparklineData}>
              <Line
                type="step"
                dataKey="val"
                stroke="#CBF900"
                strokeWidth={2}
                dot={false}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
