'use client';

import { useState } from 'react';
import { Search } from 'lucide-react';

interface ScenarioConfigProps {
  onTickerChange?: (ticker: string) => void;
  onConfigChange?: (config: any) => void;
}

export function ScenarioConfig({ onTickerChange, onConfigChange }: ScenarioConfigProps) {
  const [ticker, setTicker] = useState('NVDA');
  const [scenario, setScenario] = useState('China announces full ban on NVIDIA chip exports');
  const [speed, setSpeed] = useState(1);
  const [agentCount, setAgentCount] = useState(1000);
  const [timeHorizon, setTimeHorizon] = useState('1W');
  const [agentTypes, setAgentTypes] = useState({
    RetailTraders: true,
    HedgeFunds: true,
    NewsBots: true,
    Regulators: true,
    MarketMakers: true,
  });

  const handleTickerChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTicker = e.target.value.toUpperCase();
    setTicker(newTicker);
    onTickerChange?.(newTicker);
  };

  const handleAgentTypeToggle = (type: keyof typeof agentTypes) => {
    const newTypes = { ...agentTypes, [type]: !agentTypes[type] };
    setAgentTypes(newTypes);
    onConfigChange?.({ agentTypes: newTypes });
  };

  return (
    <div className="brutalist-card bg-white p-5 flex flex-col gap-5 relative">
      <h2 className="font-sans font-[800] text-3xl text-black uppercase tracking-tight">
        Scenario Config
      </h2>

      {/* Stock Symbol Input */}
      <div>
        <label className="block font-mono text-sm font-bold text-black uppercase mb-1">
          Target Symbol
        </label>
        <div className="relative">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-black" />
          <input
            type="text"
            value={ticker}
            onChange={handleTickerChange}
            className="w-full bg-white border-4 border-black font-mono text-lg font-bold text-black pl-10 py-2 focus:outline-none focus:shadow-[4px_4px_0px_#000000] transition-shadow"
          />
        </div>
      </div>

      {/* Scenario Textarea */}
      <div>
        <label className="block font-mono text-sm font-bold text-black uppercase mb-1">
          Scenario Description
        </label>
        <textarea
          value={scenario}
          onChange={(e) => setScenario(e.target.value)}
          className="w-full bg-white border-4 border-black font-sans text-base text-black p-3 min-h-[80px] focus:outline-none focus:shadow-[4px_4px_0px_#000000] resize-y"
        />
      </div>

      {/* Speed Slider */}
      <div>
        <div className="flex justify-between items-center mb-1">
          <label className="font-mono text-sm font-bold text-black uppercase">Simulation Speed</label>
          <span className="font-mono text-sm font-bold text-black">{speed}x</span>
        </div>
        <input
          type="range"
          min="1"
          max="10"
          value={speed}
          onChange={(e) => {
            setSpeed(Number(e.target.value));
            onConfigChange?.({ speed: Number(e.target.value) });
          }}
          className="w-full appearance-none h-3 bg-black rounded-none outline-none [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-6 [&::-webkit-slider-thumb]:h-6 [&::-webkit-slider-thumb]:bg-[#CBF900] [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:border-4 [&::-webkit-slider-thumb]:border-black [&::-webkit-slider-thumb]:cursor-pointer"
        />
      </div>

      {/* Agent Count */}
      <div>
        <label className="block font-mono text-sm font-bold text-black uppercase mb-2">
          Agent Swarm Size
        </label>
        <div className="grid grid-cols-4 gap-2">
          {[100, 500, 1000, 5000].map((count) => (
            <button
              key={count}
              onClick={() => {
                setAgentCount(count);
                onConfigChange?.({ agentCount: count });
              }}
              className={`brutalist-pill py-1.5 font-mono text-xs font-bold ${
                agentCount === count ? 'bg-black text-white' : 'bg-white text-black'
              }`}
            >
              {count}
            </button>
          ))}
        </div>
      </div>

      {/* Time Horizon */}
      <div>
        <label className="block font-mono text-sm font-bold text-black uppercase mb-2">
          Time Horizon
        </label>
        <div className="grid grid-cols-4 gap-2">
          {['1D', '1W', '1M', '6M'].map((horizon) => (
            <button
              key={horizon}
              onClick={() => {
                setTimeHorizon(horizon);
                onConfigChange?.({ timeHorizon: horizon });
              }}
              className={`brutalist-pill py-1.5 font-mono text-xs font-bold ${
                timeHorizon === horizon ? 'bg-black text-white' : 'bg-white text-black'
              }`}
            >
              {horizon}
            </button>
          ))}
        </div>
      </div>

      {/* Agent Toggles */}
      <div>
        <label className="block font-mono text-sm font-bold text-black uppercase mb-2">
          Agent Types
        </label>
        <div className="flex flex-col gap-3">
          {(Object.keys(agentTypes) as Array<keyof typeof agentTypes>).map((type) => (
            <label key={type} className="flex items-center justify-between cursor-pointer group">
              <span className="font-mono text-sm font-bold text-black uppercase">
                {type.replace(/([A-Z])/g, ' $1').trim()}
              </span>
              <div
                className={`w-12 h-6 border-[3px] border-black rounded-full relative transition-colors ${
                  agentTypes[type] ? 'bg-[#CBF900]' : 'bg-white'
                }`}
                onClick={() => handleAgentTypeToggle(type)}
              >
                <div
                  className={`absolute top-0.5 w-[14px] h-[14px] bg-black rounded-full transition-transform ${
                    agentTypes[type] ? 'left-[26px]' : 'left-0.5'
                  }`}
                />
              </div>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
}
