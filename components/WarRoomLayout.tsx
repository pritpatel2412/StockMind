'use client';

import { ReactNode } from 'react';

interface WarRoomLayoutProps {
  topBar: ReactNode;
  leftPanel: ReactNode;
  centerPanel: ReactNode;
  rightPanel: ReactNode;
  bottomBar: ReactNode;
}

export function WarRoomLayout({
  topBar,
  leftPanel,
  centerPanel,
  rightPanel,
  bottomBar,
}: WarRoomLayoutProps) {
  return (
    <div className="flex flex-col w-screen h-screen overflow-hidden bg-black text-white font-sans selection:bg-[#E87BE9] selection:text-black">
      {/* Top Bar - Zone 0 */}
      <div className="flex-none h-[64px] bg-[#000000] border-b-[3px] border-black z-10 w-full shadow-[0px_4px_0px_#000000]">
        {topBar}
      </div>

      {/* Main 3-Zone Layout */}
      <div className="flex flex-1 overflow-hidden w-full">
        {/* Left Panel - Zone 1 */}
        <div className="flex-none w-[28%] h-full bg-[#CBF900] grid-bg overflow-y-auto border-r-[3px] border-black p-4 layout-scroll">
          {leftPanel}
        </div>

        {/* Center Panel - Zone 2 */}
        <div className="flex-none w-[42%] h-full bg-[#000000] overflow-y-auto p-4 layout-scroll">
          {centerPanel}
        </div>

        {/* Right Panel - Zone 3 */}
        <div className="flex-none w-[30%] h-full bg-[#A56DFC] grid-bg-purple overflow-y-auto border-l-[3px] border-black p-4 layout-scroll">
          {rightPanel}
        </div>
      </div>

      {/* Bottom Status Bar - Zone 4 */}
      <div className="flex-none h-[40px] bg-[#000000] border-t-[3px] border-black z-10 w-full overflow-hidden">
        {bottomBar}
      </div>
    </div>
  );
}
