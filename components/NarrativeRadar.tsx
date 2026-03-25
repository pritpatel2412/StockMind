'use client';

import { motion } from 'framer-motion';
import { NewsItem } from '@/lib/types';
import { formatTime, truncate } from '@/lib/utils-helpers';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface NarrativeRadarProps {
  news: NewsItem[];
  isLoading?: boolean;
}

export function NarrativeRadar({ news, isLoading }: NarrativeRadarProps) {
  if (isLoading || !news || news.length === 0) {
    return (
      <div className="glass rounded-lg p-4 h-96 flex items-center justify-center">
        <div className="text-[#999999] text-sm">Loading news...</div>
      </div>
    );
  }

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'bullish':
        return <TrendingUp size={14} className="text-[#00ff88]" />;
      case 'bearish':
        return <TrendingDown size={14} className="text-[#ff1744]" />;
      default:
        return <Minus size={14} className="text-[#00aaff]" />;
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'bullish':
        return 'border-[#00ff88] bg-[#00ff8808]';
      case 'bearish':
        return 'border-[#ff1744] bg-[#ff174408]';
      default:
        return 'border-[#00aaff] bg-[#00aaff08]';
    }
  };

  return (
    <div className="glass rounded-lg p-4 h-96 overflow-y-auto space-y-3">
      <div className="text-xs font-mono text-[#999999] sticky top-0 bg-[#0a0a0a] py-2">
        Market Narrative
      </div>
      {news.map((item, idx) => (
        <motion.div
          key={item.id}
          className={`glass-sm border rounded-lg p-3 ${getSentimentColor(item.sentiment)}`}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: idx * 0.05 }}
        >
          <div className="flex items-start gap-2 mb-2">
            {getSentimentIcon(item.sentiment)}
            <div className="flex-1 min-w-0">
              <div className="text-xs font-mono text-[#ffffff] leading-tight">
                {truncate(item.title, 40)}
              </div>
              <div className="text-xs text-[#666666] mt-1">
                {item.source} • {formatTime(item.timestamp)}
              </div>
            </div>
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="text-xs text-[#999999]">Impact: {item.impact}/10</span>
            <div className="w-16 h-1 bg-[#ffffff05] rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-[#00ff88] to-[#ff1744]"
                style={{ width: `${item.impact * 10}%` }}
              />
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
