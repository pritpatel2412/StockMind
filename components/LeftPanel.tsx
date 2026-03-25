'use client';

import { SimulationData } from '@/lib/types';
import { ScenarioConfig } from './ScenarioConfig';
import { AgentSwarmStatus } from './AgentSwarmStatus';

interface LeftPanelProps {
  simulation?: SimulationData | null;
  onTickerChange?: (ticker: string) => void;
  onConfigChange?: (config: any) => void;
}

export function LeftPanel({ simulation, onTickerChange, onConfigChange }: LeftPanelProps) {
  return (
    <div className="flex flex-col gap-6 w-full pb-8">
      <ScenarioConfig onTickerChange={onTickerChange} onConfigChange={onConfigChange} />
      <AgentSwarmStatus simulation={simulation} />
    </div>
  );
}
