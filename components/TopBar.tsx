'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { ChevronDown, RotateCcw, Zap } from 'lucide-react';
import { PRESET_SCENARIOS } from '@/lib/mock-data';

interface TopBarProps {
  isRunning?: boolean;
  onStartSimulation?: () => void;
  onReset?: () => void;
  onScenarioChange?: (scenario: string) => void;
}

export function TopBar({
  isRunning = false,
  onStartSimulation,
  onReset,
  onScenarioChange,
}: TopBarProps) {
  const [selectedScenario, setSelectedScenario] = useState('Base Case');
  const [showDropdown, setShowDropdown] = useState(false);

  const handleScenarioSelect = (scenario: string) => {
    setSelectedScenario(scenario);
    onScenarioChange?.(scenario);
    setShowDropdown(false);
  };

  return (
    <div className="flex items-center justify-between px-6 w-full h-full">
      {/* Left: Logo */}
      <div className="flex items-center gap-2 font-sans font-[800] text-3xl tracking-tight uppercase">
        <span className="text-white">STOCK</span>
        <span className="text-[#CBF900]">MIND</span>
        <span className="text-[#CBF900] ml-1">⚡</span>
      </div>

      {/* Center: Status Sticker */}
      <div className="sticker-badge bg-white px-4 py-1.5 flex items-center gap-2 transform -rotate-1 relative group">
        <motion.div
          className={`w-3 h-3 rounded-full border-2 border-black ${
            isRunning ? 'bg-[#CBF900]' : 'bg-[#999999]'
          }`}
          animate={{ opacity: isRunning ? [1, 0.4, 1] : 1 }}
          transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
        />
        <span className="text-black text-sm pt-1">
          {isRunning ? 'SIMULATION RUNNING' : 'IDLE'}
        </span>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-4">
        {/* Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowDropdown(!showDropdown)}
            className="brutalist-button bg-white text-black px-4 py-2 font-mono text-sm font-bold uppercase flex items-center gap-2"
          >
            <span>{selectedScenario}</span>
            <ChevronDown size={18} className="text-[#A56DFC]" />
          </button>

          {showDropdown && (
            <div className="absolute top-full right-0 mt-2 w-64 brutalist-card bg-white z-50 flex flex-col">
              {PRESET_SCENARIOS.map((scenario, idx) => (
                <button
                  key={idx}
                  onClick={() => handleScenarioSelect(scenario.name)}
                  className="w-full text-left px-4 py-3 border-b-2 border-black last:border-b-0 hover:bg-[#CBF900] transition-colors"
                >
                  <div className="font-sans font-bold text-black uppercase">{scenario.name}</div>
                  <div className="font-mono text-xs text-black/70 mt-1 line-clamp-1">{scenario.description}</div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Reset Button */}
        <button
          onClick={onReset}
          className="brutalist-button bg-white text-black px-4 py-2 font-mono text-sm font-bold uppercase flex items-center gap-2"
        >
          <RotateCcw size={16} />
          RESET
        </button>

        {/* Run Button */}
        <button
          onClick={onStartSimulation}
          className="brutalist-button bg-[#CBF900] text-black px-6 py-2 font-mono text-sm font-bold uppercase flex items-center gap-2"
        >
          <Zap size={16} />
          {isRunning ? 'RUNNING...' : 'RUN SIMULATION'}
        </button>
      </div>
    </div>
  );
}
