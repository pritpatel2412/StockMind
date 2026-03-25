'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Settings, Server, Cpu, Database, Save, ShieldAlert, Globe, Bell } from 'lucide-react';

export default function SettingsPage() {
  const [apiKey, setApiKey] = useState('********************************');
  
  return (
    <div className="min-h-screen bg-black text-white px-6 pb-20 italic">
      <div className="max-w-4xl mx-auto pt-20">
        <header className="mb-16">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
             className="mb-6 inline-flex items-center gap-2 px-3 py-1 bg-[#CBF900]/10 border border-[#CBF900]/20 rounded-full"
          >
             <Settings className="w-3 h-3 text-[#CBF900]" />
             <span className="text-[10px] font-bold text-[#CBF900] tracking-widest uppercase italic">Operational Configuration</span>
          </motion.div>
          <h1 className="text-5xl md:text-7xl font-silkscreen mb-6 tracking-tighter uppercase italic">
            CORE <span className="text-[#CBF900]">SETTINGS</span>
          </h1>
        </header>

        <div className="space-y-8 italic">
          {/* AI Configuration */}
          <section className="p-8 bg-zinc-900/30 border border-zinc-800 rounded-sm">
             <div className="flex items-center gap-3 mb-8">
                <Cpu className="w-5 h-5 text-[#CBF900]" />
                <h2 className="text-xl font-silkscreen tracking-widest uppercase italic">Inference Engine</h2>
             </div>

             <div className="space-y-6">
                <div>
                  <label className="block text-[10px] font-black text-zinc-500 tracking-widest uppercase italic mb-2 italic">LLM PROVIDER</label>
                  <select className="w-full bg-black border border-zinc-800 p-4 text-sm font-bold tracking-widest uppercase italic rounded-sm focus:border-[#CBF900] outline-none">
                     <option>GROQ AI (llama-3.3-70b)</option>
                     <option>NVIDIA NIM (LLAMA-3)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-[10px] font-black text-zinc-500 tracking-widest uppercase italic mb-2 italic">API KEY (ENCRYPTED)</label>
                  <div className="flex gap-2">
                     <input 
                       type="password" 
                       value={apiKey}
                       onChange={(e) => setApiKey(e.target.value)}
                       className="flex-1 bg-black border border-zinc-800 p-4 text-sm font-mono tracking-widest uppercase italic rounded-sm focus:border-[#CBF900] outline-none" 
                     />
                     <button className="px-6 bg-zinc-800 hover:bg-zinc-700 transition-colors text-xs font-black uppercase italic italic">Update</button>
                  </div>
                </div>
             </div>
          </section>

          {/* Network Configuration */}
          <section className="p-8 bg-zinc-900/30 border border-zinc-800 rounded-sm italic">
             <div className="flex items-center gap-3 mb-8 italic">
                <Globe className="w-5 h-5 text-[#CBF900]" />
                <h2 className="text-xl font-silkscreen tracking-widest uppercase italic italic">Network Protocol</h2>
             </div>

             <div className="grid grid-cols-1 md:grid-cols-2 gap-6 italic">
                <div className="flex items-center justify-between p-4 bg-black border border-zinc-800 rounded-sm italic">
                   <div>
                      <div className="text-xs font-bold tracking-widest uppercase italic">Auto-Reconnect</div>
                      <div className="text-[9px] text-zinc-500 uppercase italic">Re-establish broken websockets</div>
                   </div>
                   <div className="w-12 h-6 bg-[#CBF900] rounded-full relative p-1 cursor-pointer">
                      <div className="w-4 h-4 bg-black rounded-full absolute right-1 shadow-sm shadow-black italic" />
                   </div>
                </div>

                <div className="flex items-center justify-between p-4 bg-black border border-zinc-800 rounded-sm italic">
                   <div>
                      <div className="text-xs font-bold tracking-widest uppercase italic">Debug Logging</div>
                      <div className="text-[9px] text-zinc-500 uppercase italic">Verbose terminal output</div>
                   </div>
                   <div className="w-12 h-6 bg-zinc-800 rounded-full relative p-1 cursor-pointer">
                      <div className="w-4 h-4 bg-zinc-600 rounded-full absolute left-1 italic shadow-sm" />
                   </div>
                </div>
             </div>
          </section>

          {/* Dangerous Zone */}
          <section className="p-8 bg-red-950/10 border border-red-900/30 rounded-sm italic">
             <div className="flex items-center gap-3 mb-8 italic">
                <ShieldAlert className="w-5 h-5 text-red-500 italic" />
                <h2 className="text-xl font-silkscreen tracking-widest uppercase italic text-red-500 italic">Danger Zone</h2>
             </div>
             
             <button className="w-full py-4 border-2 border-red-900/50 text-red-500 font-black tracking-widest hover:bg-red-500/10 transition-colors uppercase italic rounded-sm italic">
                Factory Reset Simulation Database
             </button>
          </section>

          <div className="flex justify-end pt-8 italic italic">
             <button className="px-12 py-5 bg-[#CBF900] text-black font-black tracking-[0.2em] hover:scale-105 transition-all uppercase italic rounded-sm shadow-[0_0_40px_-10px_#CBF900] flex items-center gap-3 italic">
                <Save className="w-5 h-5" />
                Commit Changes
             </button>
          </div>
        </div>
      </div>
    </div>
  );
}
