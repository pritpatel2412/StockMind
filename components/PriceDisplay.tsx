'use client';

import { SimulationData } from '@/lib/types';
import { motion } from 'framer-motion';

interface PriceDisplayProps {
  simulation?: SimulationData | null;
  isLoading?: boolean;
}

export function PriceDisplay({ simulation, isLoading }: PriceDisplayProps) {
  if (isLoading || !simulation) {
    return (
      <div className="brutalist-card bg-black p-6 flex flex-col items-center justify-center min-h-[160px]">
        <div className="font-mono text-[#E87BE9] uppercase animate-pulse">Initializing Pricing Engine...</div>
      </div>
    );
  }

  const { currentPrice, priceChange, priceChangePct, predictions } = simulation;
  const isUp = priceChange >= 0;
  const priceColor = isUp ? 'text-[#CBF900]' : 'text-[#E87BE9]';
  const badgeColor = isUp ? 'bg-[#CBF900]' : 'bg-[#E87BE9]';

  return (
    <div className="brutalist-card bg-black p-6 border-[3px] border-[#CBF900] shadow-[0px_0px_20px_rgba(203,249,0,0.15)] relative">
      <div className="flex items-start justify-between">
        <div className="flex flex-col">
          <span className="font-mono text-sm font-bold text-white uppercase tracking-widest mb-1">
            Current Price
          </span>
          <div className="flex items-center gap-4">
            <motion.div
              key={currentPrice}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`font-sans font-[800] text-6xl tracking-tighter ${priceColor}`}
            >
              ${currentPrice.toFixed(2)}
            </motion.div>
            
            <div className={`sticker-badge ${badgeColor} text-black px-3 py-1 flex items-center shadow-[2px_2px_0px_#FFFFFF] mt-2`}>
              {isUp ? '↑' : '↓'} {Math.abs(priceChangePct).toFixed(2)}%
            </div>
          </div>
        </div>
      </div>

      <div className="h-[2px] w-full bg-[#222222] my-4" />

      <div className="flex items-center justify-between mt-2">
        <div className="flex flex-col">
          <span className="font-mono text-xs font-bold text-white/50 uppercase">Target High</span>
          <span className="font-mono text-xl font-bold text-[#CBF900]">
            ${predictions.predictedHigh.toFixed(2)}
          </span>
        </div>

        <div className="flex flex-col">
          <span className="font-mono text-xs font-bold text-white/50 uppercase">Target Low</span>
          <span className="font-mono text-xl font-bold text-[#E87BE9]">
            ${predictions.predictedLow.toFixed(2)}
          </span>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex flex-col text-right">
            <span className="font-mono text-xs font-bold text-white/50 uppercase">AI Confidence</span>
            <span className="font-mono text-lg font-bold text-[#A56DFC]">
              {predictions.confidenceScore.toFixed(1)}%
            </span>
          </div>
          {/* Circular Progress */}
          <div className="relative w-12 h-12">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
              <path
                className="text-[#222222]"
                strokeWidth="4"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                className="text-[#CBF900]"
                strokeWidth="4"
                strokeDasharray={`${predictions.confidenceScore}, 100`}
                strokeLinecap="square"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
