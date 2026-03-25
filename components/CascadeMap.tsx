'use client';

import { CascadeNode } from '@/lib/types';
import { motion } from 'framer-motion';

interface CascadeMapProps {
  cascadeMap: CascadeNode[];
  isLoading?: boolean;
}

export function CascadeMap({ cascadeMap, isLoading }: CascadeMapProps) {
  if (isLoading || !cascadeMap.length) {
    return (
      <div className="brutalist-card bg-white p-4 flex flex-col items-center justify-center min-h-[300px]">
        <div className="font-mono text-black uppercase animate-pulse">Mapping cascades...</div>
      </div>
    );
  }

  // Find center node (target stock)
  const centerNode = cascadeMap.find((n) => n.type === 'target');
  const surroundingNodes = cascadeMap.filter((n) => n.type !== 'target');

  // Hardcode center layout parameters
  const centerX = 200;
  const centerY = 150;
  const radius = 100;

  return (
    <div className="brutalist-card bg-black p-4 h-[350px] relative overflow-hidden flex items-center justify-center">
      <svg width="400" height="300" viewBox="0 0 400 300" className="absolute inset-0 m-auto">
        <defs>
          <filter id="glowPositive" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        {/* Edges */}
        {surroundingNodes.map((node, i) => {
          const angle = (i / surroundingNodes.length) * 2 * Math.PI;
          const x = centerX + radius * Math.cos(angle);
          const y = centerY + radius * Math.sin(angle);
          
          let strokeProps = {};
          if (node.direction === 'positive') strokeProps = { stroke: '#CBF900', strokeWidth: 3 };
          else if (node.direction === 'negative') strokeProps = { stroke: '#E87BE9', strokeWidth: 3 };
          else strokeProps = { stroke: '#ffffff', strokeWidth: 2, strokeDasharray: '4 4' };

          return (
            <motion.line
              key={`edge-${node.id}`}
              x1={centerX}
              y1={centerY}
              x2={x}
              y2={y}
              {...strokeProps}
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 1, type: 'spring' }}
            />
          );
        })}

        {/* Surrounding Nodes */}
        {surroundingNodes.map((node, i) => {
          const angle = (i / surroundingNodes.length) * 2 * Math.PI;
          const x = centerX + radius * Math.cos(angle);
          const y = centerY + radius * Math.sin(angle);
          
          let bg = '#ffffff';
          if (node.direction === 'positive') bg = '#CBF900';
          else if (node.direction === 'negative') bg = '#E87BE9';
          
          const isHighImpact = Math.abs(node.impactScore) > 0.7;
          const pulseAnim = isHighImpact ? { scale: [1, 1.1, 1], transition: { repeat: Infinity, duration: 1.5 } } : {};

          return (
            <motion.g key={`node-${node.id}`} animate={pulseAnim as any}>
              <circle
                cx={x}
                cy={y}
                r="30"
                fill={bg}
                stroke="#000000"
                strokeWidth="3"
                filter={isHighImpact && node.direction === 'positive' ? 'url(#glowPositive)' : ''}
              />
              <text
                x={x}
                y={y}
                textAnchor="middle"
                alignmentBaseline="middle"
                className="font-sans font-[700] text-xs fill-black uppercase"
              >
                {node.label}
              </text>
            </motion.g>
          );
        })}

        {/* Center Node */}
        {centerNode && (
          <motion.g
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          >
            <circle cx={centerX} cy={centerY} r="35" fill="#CBF900" stroke="#000000" strokeWidth="3" />
            <text
              x={centerX}
              y={centerY}
              textAnchor="middle"
              alignmentBaseline="middle"
              className="font-sans font-[800] text-xl fill-black"
            >
              {centerNode.label}
            </text>
          </motion.g>
        )}
      </svg>
    </div>
  );
}
