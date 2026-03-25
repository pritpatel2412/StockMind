import { SimulationData, NewsItem, AgentAction, CascadeNode, PricePoint } from './types';

export const PRESET_SCENARIOS = [
  { name: 'China ban NVIDIA', description: 'China announces full ban on NVIDIA chip exports' },
  { name: 'Fed rate hike', description: 'Federal Reserve raises interest rates by 1%' },
  { name: 'Apple recall', description: 'Apple announces product recall affecting 10M units' },
  { name: 'Oil hits $150', description: 'Oil prices hit $150 per barrel' },
  { name: 'Bank crisis', description: 'Major bank announces liquidity crisis' },
];

export function generateInitialSimulation(ticker: string): SimulationData {
  return {
    id: `sim_mock_${Date.now()}`,
    timestamp: Date.now(),
    status: 'idle',
    currentTick: 0,
    totalTicks: 500,
    currentPrice: 135.24,
    priceChange: 0,
    priceChangePct: 0,
    priceHistory: Array.from({ length: 40 }).map((_, i) => ({
      time: `10:${i.toString().padStart(2, '0')}`,
      historical: 135 + Math.sin(i * 0.2) * 2,
      simulated: null,
      bull: null,
      bear: null,
      volume: 10000 + Math.random() * 5000,
    })),
    circuitBreaker: false,
    sentiment: { bullish: 300, neutral: 500, bearish: 200 },
    predictions: {
      bullProbability: 35.5,
      neutralProbability: 40.2,
      bearProbability: 24.3,
      predictedHigh: 142.50,
      predictedLow: 128.00,
      confidenceScore: 68.5,
    },
    totalAgents: 1000,
  };
}

export function updateSimulationTick(prev: SimulationData, newTick: number): SimulationData {
  const tickMultiplier = Math.sin(newTick * 0.1);
  const newPrice = prev.currentPrice + tickMultiplier * 0.5 + (Math.random() - 0.5) * 0.2;
  const change = newPrice - 135.24;
  
  const lastTime = prev.priceHistory[prev.priceHistory.length - 1].time;
  const [h, m] = lastTime.split(':').map(Number);
  const nextMin = (m + 1) % 60;
  const nextHr = nextMin === 0 ? h + 1 : h;
  const newTime = `${nextHr.toString().padStart(2, '0')}:${nextMin.toString().padStart(2, '0')}`;

  const newHist = [...prev.priceHistory.slice(1), {
    time: newTime,
    historical: null,
    simulated: newPrice,
    bull: newPrice * 1.05,
    bear: newPrice * 0.95,
    volume: 15000 + Math.random() * 10000,
  }];

  return {
    ...prev,
    currentTick: newTick,
    timestamp: Date.now(),
    currentPrice: newPrice,
    priceChange: change,
    priceChangePct: (change / 135.24) * 100,
    priceHistory: newHist,
    sentiment: {
      bullish: prev.sentiment.bullish + (Math.random() > 0.5 ? 5 : -5),
      neutral: prev.sentiment.neutral + (Math.random() > 0.5 ? 5 : -5),
      bearish: prev.sentiment.bearish + (Math.random() > 0.5 ? 5 : -5),
    }
  };
}

export function generateMockNews(): NewsItem[] {
  return [
    { id: '1', headline: "China announces full ban on NVIDIA chip exports", sentiment: "BEARISH", impactScore: 9, source: "Bloomberg", timestamp: new Date().toISOString() },
    { id: '2', headline: "Global semiconductor shortage worsens", sentiment: "BEARISH", impactScore: 7, source: "Reuters", timestamp: new Date(Date.now() - 60000).toISOString() },
    { id: '3', headline: "NVIDIA CEO announces emergency board meeting", sentiment: "NEUTRAL", impactScore: 5, source: "CNBC", timestamp: new Date(Date.now() - 120000).toISOString() },
    { id: '4', headline: "Analysts downgrade semiconductor sector to underweight", sentiment: "BEARISH", impactScore: 8, source: "WSJ", timestamp: new Date(Date.now() - 300000).toISOString() },
  ];
}

export function generateCascadeMap(ticker: string): CascadeNode[] {
  return [
    { id: 'center', label: ticker, type: 'target', impactScore: -0.9, direction: 'negative' },
    { id: 'tsm', label: 'TSM', type: 'supplier', impactScore: -0.8, direction: 'negative' },
    { id: 'asml', label: 'ASML', type: 'supplier', impactScore: -0.6, direction: 'negative' },
    { id: 'amd', label: 'AMD', type: 'competitor', impactScore: 0.4, direction: 'positive' },
    { id: 'intc', label: 'INTC', type: 'competitor', impactScore: 0.2, direction: 'positive' },
    { id: 'smh', label: 'SMH', type: 'etf', impactScore: -0.7, direction: 'negative' },
    { id: 'qqq', label: 'QQQ', type: 'macro', impactScore: -0.3, direction: 'negative' },
  ];
}

export function generateMockAgentActions(): AgentAction[] {
  return []; // Uses default mock array in BottomStatusBar if empty
}
