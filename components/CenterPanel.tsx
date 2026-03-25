'use client';

import { SimulationData } from '@/lib/types';
import { PriceDisplay } from './PriceDisplay';
import { PriceChart } from './PriceChart';
import { ProbabilityCurves } from './ProbabilityCurves';
import { VolumeChart } from './VolumeChart';

interface CenterPanelProps {
  simulation: SimulationData | null;
  isLoading?: boolean;
}

export function CenterPanel({ simulation, isLoading }: CenterPanelProps) {
  return (
    <div className="flex flex-col gap-6 w-full pb-8">
      {/* Circuit Breaker Alert (if active) */}
      {simulation?.circuitBreaker ? (
        <div className="bg-[#E87BE9] text-black border-[3px] border-black shadow-[4px_4px_0px_#000000] p-3 flex items-center justify-center font-mono font-bold uppercase text-lg animate-pulse">
          ⛔ CIRCUIT BREAKER ACTIVE — TRADING HALTED
        </div>
      ) : null}

      <PriceDisplay simulation={simulation} isLoading={isLoading} />
      <PriceChart simulation={simulation} isLoading={isLoading} />
      <ProbabilityCurves simulation={simulation} isLoading={isLoading} />
      <VolumeChart simulation={simulation} isLoading={isLoading} />
    </div>
  );
}
