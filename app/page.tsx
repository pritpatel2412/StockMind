'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Shield, Brain, Zap, Activity, ChevronRight, BarChart3, Globe, Lock } from 'lucide-react';

const features = [
  {
    title: "AI Agent Swarm",
    desc: "100+ autonomous trading agents operating in real-time simulation using Groq-powered LLMs.",
    icon: Brain
  },
  {
    title: "Market War Room",
    desc: "A decision-support dashboard built for rapid analysis of complex market sentiment shifts.",
    icon: BarChart3
  },
  {
    title: "Real-time Cascades",
    desc: "Watch market trends evolve and propagate through the agent network with pinpoint visual tools.",
    icon: Zap
  },
  {
    title: "Narrative Engine",
    desc: "AI-driven news generation and sentiment analysis that creates realistic market storytelling.",
    icon: Globe
  }
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* Dynamic Background */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-0 left-0 w-full h-[600px] bg-gradient-to-b from-[#CBF900]/10 to-transparent pointer-events-none" />
        <div className="grid-bg opacity-30 absolute inset-0" />
      </div>

      <main className="relative z-10 pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#CBF900]/10 border border-[#CBF900]/20 text-[#CBF900] text-xs font-black tracking-widest mb-8 uppercase italic italic">
              <Activity className="w-3 h-3 animate-pulse" />
              Next-Gen Market Simulation Engine
            </div>
            
            <h1 className="text-6xl md:text-8xl font-silkscreen tracking-tighter mb-8 leading-none">
              MARKET <span className="text-[#CBF900]">SENTIMENT</span> <br /> 
              WAR ROOM
            </h1>
            
            <p className="max-w-2xl mx-auto text-xl text-zinc-400 mb-12 font-medium leading-relaxed">
              Experience the future of financial analysis. A high-fidelity simulation of 
              autonomous AI agents battling for market supremacy in real-time.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
              <Link href="/simulation">
                <button className="px-10 py-5 bg-[#CBF900] text-black font-black text-lg tracking-widest hover:scale-105 transition-all duration-300 flex items-center gap-3 uppercase italic rounded-sm shadow-[0_0_50px_-12px_#CBF900]">
                  Enter Simulation
                  <ChevronRight className="w-6 h-6" />
                </button>
              </Link>
              <button className="px-10 py-5 bg-zinc-900 border-2 border-zinc-800 text-white font-black text-lg tracking-widest hover:bg-zinc-800 transition-all uppercase italic rounded-sm">
                View Agent Swarm
              </button>
            </div>
          </motion.div>

          {/* Stats Bar */}
          <motion.div 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-32 py-10 border-y border-zinc-800/50 backdrop-blur-sm"
          >
            {[
              { val: "100+", label: "ACTIVE AGENTS" },
              { val: "1B+", label: "SIM VOLUME" },
              { val: "50MS", label: "LATENCY" },
              { val: "24/7", label: "MARKET UP" }
            ].map((stat, i) => (
              <div key={i}>
                <div className="font-silkscreen text-3xl text-[#CBF900] mb-1">{stat.val}</div>
                <div className="text-[10px] font-black tracking-widest text-zinc-500">{stat.label}</div>
              </div>
            ))}
          </motion.div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-32 text-left">
            {features.map((f, i) => {
               const Icon = f.icon;
               return (
                <motion.div 
                  key={i}
                  whileHover={{ y: -5 }}
                  className="p-8 bg-zinc-900/50 border border-zinc-800 hover:border-[#CBF900]/50 transition-colors rounded-sm"
                >
                  <div className="w-12 h-12 bg-[#CBF900]/10 border border-[#CBF900]/20 rounded-sm flex items-center justify-center mb-6">
                    <Icon className="w-6 h-6 text-[#CBF900]" />
                  </div>
                  <h3 className="font-silkscreen text-lg mb-4 text-white uppercase italic tracking-tighter">{f.title}</h3>
                  <p className="text-sm text-zinc-500 leading-relaxed font-medium">
                    {f.desc}
                  </p>
                </motion.div>
               )
            })}
          </div>

          {/* Terminal Section */}
          <motion.div 
             initial={{ opacity: 0, y: 40 }}
             whileInView={{ opacity: 1, y: 0 }}
             viewport={{ once: true }}
             className="mt-40 max-w-4xl mx-auto rounded-lg overflow-hidden border-2 border-zinc-800 shadow-2xl shadow-black shadow-[#CBF900]/10"
          >
            <div className="bg-zinc-900 px-4 py-2 flex items-center justify-between border-b border-zinc-800">
               <div className="flex gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-red-500/20" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500/20" />
                  <div className="w-3 h-3 rounded-full bg-green-500/20" />
               </div>
               <div className="text-[10px] font-black tracking-widest text-zinc-500 flex items-center gap-2 uppercase italic">
                  <Lock className="w-3 h-3" />
                  root@stockmind:~/core-engine
               </div>
            </div>
            <div className="bg-black/80 backdrop-blur-xl p-8 font-mono text-xs text-zinc-400 space-y-2 text-left">
               <p className="text-[#CBF900]">[SYSTEM] Initializing Agent Swarm v1.4.0...</p>
               <p>[INFO] Connecting to Groq High-Performance Inference Engine...</p>
               <p>[INFO] Fetching real-time market delta for ticker AAPL...</p>
               <p>[INFO] Starting 120 Hedge Fund Agent instances...</p>
               <p className="text-zinc-500 animate-pulse mt-4">_ ACCESS GRANTED. SIMULATION READY.</p>
            </div>
          </motion.div>
        </div>
      </main>

      {/* Footer */}
      <footer className="py-20 px-6 border-t border-zinc-800 mt-20">
         <div className="max-w-7xl mx-auto flex flex-col md:row items-center justify-between gap-10 opacity-50 text-[10px] font-black tracking-widest text-zinc-500 uppercase italic transition-opacity hover:opacity-100 italic italic">
            <div className="flex items-center gap-2 italic">
               <Shield className="w-4 h-4 text-[#CBF900]" />
               STOCKMIND © 2026 INTERNAL USE ONLY
            </div>
            <div className="flex gap-8 italic italic">
               <span>GOV PROTOCOL 812-B</span>
               <span>AUTH: GEMINI-3.1-PRO</span>
               <span>SYSTEM: ACTIVE</span>
            </div>
         </div>
      </footer>
    </div>
  );
}
