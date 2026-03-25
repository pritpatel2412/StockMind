'use client';

import { NewsItem, CascadeNode } from '@/lib/types';
import { NewsRadar } from './NewsRadar';
import { CascadeMap } from './CascadeMap';

interface RightPanelProps {
  news: NewsItem[];
  cascadeMap: CascadeNode[];
  isLoading?: boolean;
}

export function RightPanel({ news, cascadeMap, isLoading }: RightPanelProps) {
  return (
    <div className="flex flex-col gap-6 w-full h-[150%] pb-8">
      {/* Narrative Radar - News Feed */}
      <h2 className="font-sans font-[800] text-3xl text-white uppercase tracking-tight -mb-2">
        NARRATIVE RADAR 📡
      </h2>
      <NewsRadar news={news} isLoading={isLoading} />

      {/* Cascade Map */}
      <h2 className="font-sans font-[800] text-3xl text-white uppercase tracking-tight mt-4 -mb-2">
        CASCADE MAP 🌊
      </h2>
      <CascadeMap cascadeMap={cascadeMap} isLoading={isLoading} />
    </div>
  );
}
