'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Cpu, Zap, Activity, Users, Target, Rocket, Briefcase } from 'lucide-react';

const agentTypes = [
  {
    title: "Hedge Fund Manager",
    type: "Hedge Fund",
    desc: "Quantitative, data-driven, and highly risk-averse. Uses real-time technical analysis and SEC filings to make precise, high-volume trades.",
    icon: Briefcase,
    stats: { risk: "MEDIUM", freq: "HIGH", strategy: "ALPHA" }
  },
  {
    title: "Robinhood Retail",
    type: "Retail",
    desc: "Emotional, driven by FOMO, and quick to panic. Follows herd behavior and social sentiment spikes with aggressive position sizing.",
    icon: Zap,
    stats: { risk: "HIGH", freq: "EXTREME", strategy: "TREND" }
  },
  {
    title: "Market Maker",
    type: "Institutional",
    desc: "Provides liquidity by maintaining tight bid-ask spreads. Operates with near-zero latency to exploit arbitrage opportunities.",
    icon: Cpu,
    stats: { risk: "LOW", freq: "LIMITLESS", strategy: "FLOW" }
  },
  {
    title: "News Oracle",
    type: "Narrative",
    desc: "Analyzes breaking news and sentiment to forecast market shifts. Acts as the primary driver of information flow in the simulation.",
    icon: Target,
    stats: { risk: "NONE", freq: "STEADY", strategy: "MACRO" }
  }
];

export default function AgentsPage() {
  return (
    <div className="min-h-screen bg-black text-white px-6 pb-20">
      <div className="max-w-7xl mx-auto pt-20">
        <header className="mb-20 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
             className="mb-6 inline-flex items-center gap-2 px-3 py-1 bg-[#CBF900]/10 border border-[#CBF900]/20 rounded-full"
          >
             <Users className="w-3 h-3 text-[#CBF900]" />
             <span className="text-[10px] font-bold text-[#CBF900] tracking-widest uppercase italic">The AI Swarm Organization</span>
          </motion.div>
          <h1 className="text-5xl md:text-7xl font-silkscreen mb-6 tracking-tighter">
            AUTONOMOUS <span className="text-[#CBF900]">ENTITIES</span>
          </h1>
          <p className="max-w-2xl mx-auto text-zinc-500 font-medium">
            Explore the diverse personalities and algorithmic strategies that drive 
            the StockMind simulation engine. Every agent is a unique LLM-powered actor.
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {agentTypes.map((agent, i) => {
             const Icon = agent.icon;
             return (
               <motion.div 
                 key={agent.title}
                 initial={{ opacity: 0, scale: 0.95 }}
                 animate={{ opacity: 1, scale: 1 }}
                 transition={{ delay: i * 0.1 }}
                 className="p-8 bg-zinc-900/30 border-2 border-zinc-800 rounded-sm hover:border-[#CBF900]/40 transition-all duration-300 group"
               >
                  <div className="flex items-start justify-between mb-8">
                    <div className="w-16 h-16 bg-black border border-zinc-800 rounded-sm flex items-center justify-center group-hover:bg-[#CBF900] group-hover:text-black transition-colors duration-500">
                       <Icon className="w-8 h-8" />
                    </div>
                    <div className="text-right">
                       <div className="text-[10px] font-black tracking-widest text-[#CBF900] mb-1">{agent.type}</div>
                       <div className="flex gap-1 justify-end">
                          {[1,2,3].map(j => <div key={j} className="w-1 h-3 bg-[#CBF900]/30 rounded-full" />)}
                       </div>
                    </div>
                  </div>

                  <h3 className="text-2xl font-silkscreen mb-4 tracking-tighter uppercase italic">{agent.title}</h3>
                  <p className="text-zinc-500 text-sm leading-relaxed mb-8 font-medium">
                    {agent.desc}
                  </p>

                  <div className="grid grid-cols-3 gap-4 pt-8 border-t border-zinc-800">
                     {Object.entries(agent.stats).map(([k, v]) => (
                        <div key={k}>
                           <div className="text-[9px] font-black tracking-widest text-zinc-600 mb-1 uppercase italic">{k}</div>
                           <div className="text-xs font-bold text-white tracking-widest uppercase italic italic">{v}</div>
                        </div>
                     ))}
                  </div>
               </motion.div>
             )
          })}
        </div>
      </div>
    </div>
  );
}
