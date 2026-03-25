'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { History, BarChart2, Shield, Calendar, ArrowUpRight, ArrowDownRight } from 'lucide-react';

const mockPastSimulations = [
  { id: "SIM-8122-X", ticker: "NVDA", date: "2026-03-20", return: +12.4, status: "COMPLETED", scenario: "Bull Market" },
  { id: "SIM-9AC2-B", ticker: "TSLA", date: "2026-03-19", return: -4.2, status: "COMPLETED", scenario: "Volatile Expansion" },
  { id: "SIM-311D-A", ticker: "AAPL", date: "2026-03-18", return: +2.1, status: "COMPLETED", scenario: "Normal Market" },
  { id: "SIM-81F1-E", ticker: "BTC-USD", date: "2026-03-17", return: +24.8, status: "COMPLETED", scenario: "Hyper Cascade" },
];

export default function HistoryPage() {
  return (
    <div className="min-h-screen bg-black text-white px-6 pb-20">
      <div className="max-w-7xl mx-auto pt-20">
        <header className="mb-20 text-center">
           <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
             className="mb-8 inline-flex items-center gap-2 px-3 py-1 bg-[#CBF900]/10 border border-[#CBF900]/20 rounded-full"
          >
             <History className="w-3 h-3 text-[#CBF900]" />
             <span className="text-[10px] font-bold text-[#CBF900] tracking-widest uppercase italic">Past Simulations Archive</span>
          </motion.div>
          <h1 className="text-5xl md:text-7xl font-silkscreen mb-6 tracking-tighter uppercase italic">
            TACTICAL <span className="text-[#CBF900]">HISTORY</span>
          </h1>
          <p className="max-w-2xl mx-auto text-zinc-500 font-medium leading-relaxed">
             Review the outcomes of previous AI swarm operations. Analyze price movement 
             deltas and agent performance metrics from earlier sessions.
          </p>
        </header>

        <div className="grid grid-cols-1 gap-4 max-w-4xl mx-auto italic">
          {mockPastSimulations.map((sim, i) => (
            <motion.div 
               key={sim.id}
               initial={{ x: -20, opacity: 0 }}
               animate={{ x: 0, opacity: 1 }}
               transition={{ delay: i * 0.1 }}
               className="group flex flex-col md:flex-row items-center justify-between p-6 bg-zinc-900/50 border border-zinc-800 hover:border-[#CBF900]/30 transition-all rounded-sm cursor-pointer"
            >
               <div className="flex items-center gap-6">
                  <div className="w-14 h-14 bg-black border border-zinc-800 flex items-center justify-center font-silkscreen text-[#CBF900] tracking-tighter italic italic">
                     {sim.ticker.slice(0, 4)}
                  </div>
                  <div>
                     <div className="text-[10px] font-black text-zinc-600 tracking-widest uppercase italic mb-1 italic">Simulation ID: {sim.id}</div>
                     <h3 className="text-xl font-silkscreen text-white tracking-widest uppercase italic italic">{sim.scenario}</h3>
                  </div>
               </div>

               <div className="flex items-center gap-12 mt-6 md:mt-0 italic italic">
                  <div className="text-right italic">
                     <div className="text-[9px] font-black tracking-widest text-zinc-600 mb-1 uppercase italic italic">SESSION RETURN</div>
                     <div className={`text-xl font-silkscreen flex items-center justify-end gap-2 ${sim.return > 0 ? 'text-[#CBF900]' : 'text-red-500'}`}>
                        {sim.return > 0 ? <ArrowUpRight className="w-5 h-5" /> : <ArrowDownRight className="w-5 h-5" />}
                        {sim.return > 0 ? '+' : ''}{sim.return}%
                     </div>
                  </div>
                  <div className="text-right italic whitespace-nowrap">
                     <div className="text-[9px] font-black tracking-widest text-zinc-600 mb-1 uppercase italic italic">DATE</div>
                     <div className="text-xs font-bold text-white tracking-widest flex items-center justify-end gap-2 uppercase italic italic italic">
                        <Calendar className="w-3 h-3 text-zinc-500" />
                        {sim.date}
                     </div>
                  </div>
               </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
