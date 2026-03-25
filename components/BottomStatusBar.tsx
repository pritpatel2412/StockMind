'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

interface AgentAction {
  agent_id: string;
  agent_type: string;
  action: string;
  quantity: number;
  price_target: number;
  reasoning: string;
  timestamp: string;
}

interface BottomStatusBarProps {
  currentTick?: number;
  totalTicks?: number;
  agentActions?: AgentAction[];
  lastUpdated?: number;
}

export function BottomStatusBar({
  currentTick = 0,
  agentActions = [],
  lastUpdated = Date.now(),
}: BottomStatusBarProps) {
  const [timeAgo, setTimeAgo] = useState('0s ago');

  useEffect(() => {
    const interval = setInterval(() => {
      const seconds = Math.floor((Date.now() - lastUpdated) / 1000);
      setTimeAgo(`${seconds}s ago`);
    }, 1000);
    return () => clearInterval(interval);
  }, [lastUpdated]);

  const mockActions = [
    "🤖 HedgeFund_07 SOLD 50,000 NVDA",
    "🤖 RetailBot_443 triggered stop-loss",
    "🤖 NewsAgent detected: China export ban story impact 9/10",
    "🤖 MarketMaker_01 widened spread by 0.05",
    "🤖 RetailBot_889 bought the dip",
  ];

  const actionsToDisplay = agentActions.length > 0
    ? agentActions.map(a => `🤖 ${a.agent_id} ${a.action} ${a.quantity} shares`)
    : mockActions;

  return (
    <div className="flex items-center justify-between px-6 w-full h-[40px] bg-[#000000] overflow-hidden">
      {/* Left: Tick Counter */}
      <div className="flex-none flex items-center gap-2 w-48 border-r-2 border-[#222222] h-full pr-4">
        <span className="font-mono text-[#CBF900] text-sm uppercase font-bold tracking-widest flex items-center gap-2">
          <div className="w-2 h-2 bg-[#CBF900] animate-pulse" />
          TICK: <motion.span key={currentTick} initial={{ opacity: 0 }} animate={{ opacity: 1 }}>{currentTick.toLocaleString()}</motion.span>
        </span>
      </div>

      {/* Center: Marquee */}
      <div className="flex-1 overflow-hidden relative flex items-center h-full mx-4 mask-edges">
        <motion.div
          className="flex whitespace-nowrap gap-12"
          animate={{ x: ["0%", "-50%"] }}
          transition={{ duration: 20, ease: "linear", repeat: Infinity }}
        >
          {/* Double list for smooth infinite scroll */}
          {[...actionsToDisplay, ...actionsToDisplay].map((text, i) => (
            <span key={i} className="font-mono text-sm text-white uppercase flex items-center gap-12">
              {text} <span className="text-[#A56DFC] opacity-50">|</span>
            </span>
          ))}
        </motion.div>
      </div>

      {/* Right: Last Updated */}
      <div className="flex-none flex items-center justify-end w-48 border-l-2 border-[#222222] h-full pl-4">
        <span className="font-mono text-[#A56DFC] text-xs font-bold uppercase">
          LAST UPDATE: {timeAgo}
        </span>
      </div>
    </div>
  );
}
