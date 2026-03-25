'use client';

import { NewsItem } from '@/lib/types';
import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';

interface NewsRadarProps {
  news: NewsItem[];
  isLoading?: boolean;
}

export function NewsRadar({ news, isLoading }: NewsRadarProps) {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  if (isLoading || !news.length || !mounted) {
    return (
      <div className="brutalist-card bg-white p-4 flex flex-col items-center justify-center min-h-[200px]">
        <div className="font-mono text-black uppercase animate-pulse">Scanning news API...</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4 overflow-hidden relative">
      <AnimatePresence>
        {news.slice(0, 10).map((item) => {
          const isBullish = item.sentiment === 'BULLISH';
          const isBearish = item.sentiment === 'BEARISH';
          const bgBadgeClass = isBullish ? 'bg-[#CBF900]' : isBearish ? 'bg-[#E87BE9]' : 'bg-white';

          return (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ type: 'spring', stiffness: 200, damping: 20 }}
              className="brutalist-card bg-white flex flex-col p-4 gap-2"
            >
              {/* Header: source + badge + impact */}
              <div className="flex justify-between items-start gap-2">
                <div className="flex gap-2 items-center">
                  <span className={`sticker-badge ${bgBadgeClass} px-2 py-0.5 text-xs text-black`}>
                    {item.sentiment}
                  </span>
                  <span className="font-mono font-bold text-xs text-black/60 uppercase">
                    {item.source} • {new Date(item.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="font-mono text-xs font-bold text-black uppercase">
                  ⚡ {item.impactScore}/10
                </div>
              </div>

              {/* Headline */}
              <h3 className="font-sans font-[500] text-lg text-black leading-tight line-clamp-2 mt-1">
                {item.headline}
              </h3>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
