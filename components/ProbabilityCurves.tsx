'use client';

import { SimulationData } from '@/lib/types';
import { motion } from 'framer-motion';

interface ProbabilityCurvesProps {
  simulation?: SimulationData | null;
  isLoading?: boolean;
}

export function ProbabilityCurves({ simulation, isLoading }: ProbabilityCurvesProps) {
  if (isLoading || !simulation) {
    return (
      <div className="brutalist-card bg-black p-4 flex items-center justify-center min-h-[120px]">
        <div className="font-mono text-[#A56DFC] uppercase animate-pulse">Calculating Probabilities...</div>
      </div>
    );
  }
  const { bullProbability, neutralProbability, bearProbability, predictedHigh, predictedLow } = simulation.predictions;
  const { currentPrice } = simulation;

  return (
    <div className="brutalist-card bg-black p-5 relative border-[3px] border-black">
      <span className="sticker-badge bg-white text-black px-2 py-0.5 absolute -top-4 -left-2 rotate-2">
        SCENARIO PROBABILITIES
      </span>

      <div className="grid grid-cols-3 gap-4 mt-2">
        {/* BULLISH */}
        <div className="flex flex-col gap-2">
          <div className="flex items-end justify-between">
            <span className="font-sans font-[700] text-sm text-white uppercase tracking-wider">Bullish</span>
            <span className="font-mono text-xs text-[#CBF900]">${predictedHigh.toFixed(2)}</span>
          </div>
          <div className="w-full h-4 bg-[#222222] border-2 border-white relative overflow-hidden">
            <motion.div
              className="absolute top-0 left-0 h-full bg-[#CBF900]"
              initial={{ width: 0 }}
              animate={{ width: `${bullProbability}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          <span className="font-mono text-sm font-bold text-[#CBF900] text-right">{bullProbability.toFixed(1)}%</span>
        </div>

        {/* NEUTRAL */}
        <div className="flex flex-col gap-2">
          <div className="flex items-end justify-between">
            <span className="font-sans font-[700] text-sm text-white uppercase tracking-wider">Neutral</span>
            <span className="font-mono text-xs text-[#A56DFC]">${currentPrice.toFixed(2)}</span>
          </div>
          <div className="w-full h-4 bg-[#222222] border-2 border-white relative overflow-hidden">
            <motion.div
              className="absolute top-0 left-0 h-full bg-[#A56DFC]"
              initial={{ width: 0 }}
              animate={{ width: `${neutralProbability}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          <span className="font-mono text-sm font-bold text-[#A56DFC] text-right">{neutralProbability.toFixed(1)}%</span>
        </div>

        {/* BEARISH */}
        <div className="flex flex-col gap-2">
          <div className="flex items-end justify-between">
            <span className="font-sans font-[700] text-sm text-white uppercase tracking-wider">Bearish</span>
            <span className="font-mono text-xs text-[#E87BE9]">${predictedLow.toFixed(2)}</span>
          </div>
          <div className="w-full h-4 bg-[#222222] border-2 border-white relative overflow-hidden">
            <motion.div
              className="absolute top-0 left-0 h-full bg-[#E87BE9]"
              initial={{ width: 0 }}
              animate={{ width: `${bearProbability}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          <span className="font-mono text-sm font-bold text-[#E87BE9] text-right">{bearProbability.toFixed(1)}%</span>
        </div>
      </div>
    </div>
  );
}
