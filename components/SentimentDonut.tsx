'use client';

import { SimulationData } from '@/lib/types';
import { motion } from 'framer-motion';

interface SentimentDonutProps {
  simulation: SimulationData | null;
  isLoading?: boolean;
}

export function SentimentDonut({ simulation, isLoading }: SentimentDonutProps) {
  if (isLoading || !simulation) {
    return (
      <div className="glass rounded-lg p-4 flex items-center justify-center h-40">
        <div className="text-[#999999] text-sm">Loading sentiment...</div>
      </div>
    );
  }

  const total = simulation.sentiment.bullish + simulation.sentiment.neutral + simulation.sentiment.bearish;
  const bullishPercent = (simulation.sentiment.bullish / total) * 100;
  const neutralPercent = (simulation.sentiment.neutral / total) * 100;
  const bearishPercent = (simulation.sentiment.bearish / total) * 100;

  const circumference = 2 * Math.PI * 45;
  const bullishOffset = circumference * (1 - bullishPercent / 100);
  const neutralOffset = circumference * (1 - (bullishPercent + neutralPercent) / 100);

  return (
    <div className="glass rounded-lg p-4">
      <h3 className="text-xs font-mono text-[#00ff88] uppercase mb-4">Sentiment Breakdown</h3>

      <div className="flex items-center justify-between gap-4">
        {/* Donut Chart */}
        <div className="flex-1 flex items-center justify-center">
          <svg width="120" height="120" viewBox="0 0 120 120">
            <motion.circle
              cx="60"
              cy="60"
              r="45"
              fill="none"
              stroke="#00ff88"
              strokeWidth="12"
              strokeDasharray={circumference}
              strokeDashoffset={bullishOffset}
              strokeLinecap="round"
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset: bullishOffset }}
              transition={{ duration: 1 }}
            />
            <motion.circle
              cx="60"
              cy="60"
              r="45"
              fill="none"
              stroke="#00aaff"
              strokeWidth="12"
              strokeDasharray={circumference * (neutralPercent / 100)}
              strokeDashoffset={neutralOffset}
              strokeLinecap="round"
              style={{
                rotate: `${(bullishPercent * 360) / 100}deg`,
                transformOrigin: '60px 60px',
              }}
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset: neutralOffset }}
              transition={{ duration: 1, delay: 0.2 }}
            />
            <motion.circle
              cx="60"
              cy="60"
              r="45"
              fill="none"
              stroke="#ff1744"
              strokeWidth="12"
              strokeDasharray={circumference * (bearishPercent / 100)}
              strokeDashoffset={0}
              strokeLinecap="round"
              style={{
                rotate: `${((bullishPercent + neutralPercent) * 360) / 100}deg`,
                transformOrigin: '60px 60px',
              }}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1, delay: 0.4 }}
            />
          </svg>
        </div>

        {/* Legend */}
        <div className="flex-1 space-y-2">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[#00ff88]" />
            <div className="flex-1">
              <div className="text-xs text-[#999999]">Bullish</div>
              <div className="text-sm font-mono text-[#00ff88]">{bullishPercent.toFixed(1)}%</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[#00aaff]" />
            <div className="flex-1">
              <div className="text-xs text-[#999999]">Neutral</div>
              <div className="text-sm font-mono text-[#00aaff]">{neutralPercent.toFixed(1)}%</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[#ff1744]" />
            <div className="flex-1">
              <div className="text-xs text-[#999999]">Bearish</div>
              <div className="text-sm font-mono text-[#ff1744]">{bearishPercent.toFixed(1)}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
