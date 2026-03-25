'use client';

import { motion } from 'framer-motion';
import { CascadeNode } from '@/lib/types';

interface MarketCascadeMapProps {
  cascadeMap: CascadeNode[];
  isLoading?: boolean;
}

export function MarketCascadeMap({ cascadeMap, isLoading }: MarketCascadeMapProps) {
  if (isLoading || !cascadeMap || cascadeMap.length === 0) {
    return (
      <div className="glass rounded-lg p-4 h-64 flex items-center justify-center">
        <div className="text-[#999999] text-sm">Loading cascade map...</div>
      </div>
    );
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'bullish':
        return '#00ff88';
      case 'bearish':
        return '#ff1744';
      default:
        return '#00aaff';
    }
  };

  const targetNode = cascadeMap.find((n) => n.type === 'target');

  return (
    <div className="glass rounded-lg p-4 h-64 flex flex-col">
      <div className="text-xs font-mono text-[#999999] mb-3">Market Cascade</div>

      {/* Simple Grid Visualization */}
      <div className="flex-1 flex items-center justify-center">
        <svg width="100%" height="100%" viewBox="0 0 200 140" preserveAspectRatio="xMidYMid meet">
          {/* Draw connections */}
          {cascadeMap.map((node) => {
            if (node.type === 'target' || !targetNode) return null;

            const startX = 100;
            const startY = 70;

            // Position connected nodes around the center
            const angle = (cascadeMap.indexOf(node) * Math.PI * 2) / cascadeMap.length;
            const endX = 100 + Math.cos(angle) * 60;
            const endY = 70 + Math.sin(angle) * 50;

            const color = node.sentiment === 'bearish' ? '#ff1744' : node.sentiment === 'bullish' ? '#00ff88' : '#00aaff';

            return (
              <line
                key={`line-${node.id}`}
                x1={startX}
                y1={startY}
                x2={endX}
                y2={endY}
                stroke={color}
                strokeWidth="1"
                opacity="0.3"
              />
            );
          })}

          {/* Draw nodes */}
          {cascadeMap.map((node, idx) => {
            if (node.type === 'target') {
              // Center node
              return (
                <motion.g key={node.id}>
                  <motion.circle
                    cx="100"
                    cy="70"
                    r="8"
                    fill={getSentimentColor(node.sentiment)}
                    animate={{ r: [8, 10, 8] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                  <circle cx="100" cy="70" r="8" fill="none" stroke={getSentimentColor(node.sentiment)} strokeWidth="1" opacity="0.5" />
                  <text x="100" y="90" textAnchor="middle" fill="#ffffff" fontSize="10" fontFamily="monospace">
                    {node.label}
                  </text>
                </motion.g>
              );
            }

            // Connected nodes
            const angle = (idx * Math.PI * 2) / cascadeMap.length;
            const x = 100 + Math.cos(angle) * 60;
            const y = 70 + Math.sin(angle) * 50;

            return (
              <motion.g key={node.id}>
                <motion.circle
                  cx={x}
                  cy={y}
                  r="5"
                  fill={getSentimentColor(node.sentiment)}
                  animate={{ opacity: [0.6, 1, 0.6] }}
                  transition={{ duration: 3, repeat: Infinity }}
                />
                <text
                  x={x}
                  y={y - 8}
                  textAnchor="middle"
                  fill="#999999"
                  fontSize="8"
                  fontFamily="monospace"
                >
                  {node.label}
                </text>
              </motion.g>
            );
          })}
        </svg>
      </div>

      {/* Legend */}
      <div className="mt-3 pt-3 border-t border-[#ffffff10] flex gap-3 text-xs">
        <div className="flex items-center gap-1">
          <div className="w-2 h-2 rounded-full bg-[#00ff88]" />
          <span className="text-[#666666]">Bull</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2 h-2 rounded-full bg-[#00aaff]" />
          <span className="text-[#666666]">Neutral</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2 h-2 rounded-full bg-[#ff1744]" />
          <span className="text-[#666666]">Bear</span>
        </div>
      </div>
    </div>
  );
}
