'use client';

import { useState, useEffect } from 'react';
import { WarRoomLayout } from '@/components/WarRoomLayout';
import { TopBar } from '@/components/TopBar';
import { LeftPanel } from '@/components/LeftPanel';
import { CenterPanel } from '@/components/CenterPanel';
import { RightPanel } from '@/components/RightPanel';
import { BottomStatusBar } from '@/components/BottomStatusBar';
import {
  generateInitialSimulation,
  generateMockNews,
  generateMockAgentActions,
  generateCascadeMap,
  updateSimulationTick,
} from '@/lib/mock-data';
import { SimulationData } from '@/lib/types';
import { useSimulation } from '@/hooks/useSimulation';

export default function Home() {
  const [simulationId, setSimulationId] = useState<string | null>(null);
  
  // Custom Hook for WebSocket connection to the backend
  const { data: realSimulation, status: wsStatus, disconnect } = useSimulation(simulationId);
  
  // Use mock simulation as fallback when disconnected/idle
  const [mockSimulation, setMockSimulation] = useState<SimulationData | null>(null);
  const [isRunningMock, setIsRunningMock] = useState(false);
  const [currentTick, setCurrentTick] = useState(0);
  const [ticker, setTicker] = useState('NVDA');

  const [simConfig, setSimConfig] = useState({});

  useEffect(() => {
    const initial = generateInitialSimulation(ticker);
    setMockSimulation(initial);
  }, [ticker]);

  // Handle mock simulation ticks if real simulation is not running
  useEffect(() => {
    if (!isRunningMock || !mockSimulation || wsStatus === 'connected') return;

    const interval = setInterval(() => {
      setCurrentTick((prev) => {
        const next = prev + 1;
        if (next > mockSimulation.totalTicks) {
          setIsRunningMock(false);
          return prev;
        }
        setMockSimulation((prevSim) => prevSim ? updateSimulationTick(prevSim, next) : prevSim);
        return next;
      });
    }, 500); 

    return () => clearInterval(interval);
  }, [isRunningMock, mockSimulation, wsStatus]);

  const handleStartSimulation = async () => {
    // Attempt backend start. Fallback to mock if API unavailable.
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/simulation/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stock_symbol: ticker, ...simConfig }),
      });
      if (response.ok) {
        const { simulation_id } = await response.json();
        setSimulationId(simulation_id);
        return;
      }
    } catch (e) {
      console.warn("Backend unavailable, starting mock simulation.", e);
    }
    
    // Fallback to mock simulation
    setIsRunningMock(true);
    setCurrentTick(0);
  };

  const handleReset = () => {
    setIsRunningMock(false);
    setCurrentTick(0);
    disconnect();
    setSimulationId(null);
    setMockSimulation(generateInitialSimulation(ticker));
  };

  const activeSimulation = (wsStatus === 'connected' && realSimulation) ? realSimulation : mockSimulation;
  const isRunning = (wsStatus === 'connected') || isRunningMock;
  const tick = activeSimulation?.timestamp ? currentTick : 0; // fallback simplified logic

  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <WarRoomLayout
      topBar={
        <TopBar
          isRunning={isRunning}
          onStartSimulation={handleStartSimulation}
          onReset={handleReset}
        />
      }
      leftPanel={
        <LeftPanel 
          simulation={activeSimulation} 
          onTickerChange={setTicker} 
          onConfigChange={(newConfig) => setSimConfig({ ...simConfig, ...newConfig })} 
        />
      }
      centerPanel={<CenterPanel simulation={activeSimulation} />}
      rightPanel={
        <RightPanel
          news={generateMockNews()} // Fallback if activeSimulation doesn't have it
          cascadeMap={generateCascadeMap(ticker)} // Fallback
        />
      }
      bottomBar={
        <BottomStatusBar
          currentTick={activeSimulation?.currentTick || tick}
          totalTicks={activeSimulation?.totalTicks || 100}
          agentActions={generateMockAgentActions()}
          lastUpdated={activeSimulation?.timestamp || Date.now()}
        />
      }
    />
  );
}
