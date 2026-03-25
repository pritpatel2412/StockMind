export type SimulationStatus = 'idle' | 'running' | 'completed' | 'error';
export type SentimentType = 'BULLISH' | 'NEUTRAL' | 'BEARISH';

export interface PricePoint {
  time: string;
  historical: number | null;
  simulated: number | null;
  bull: number | null;
  bear: number | null;
  volume: number;
}

export interface Predictions {
  bullProbability: number;
  neutralProbability: number;
  bearProbability: number;
  predictedHigh: number;
  predictedLow: number;
  confidenceScore: number;
}

export interface SimulationData {
  id: string;
  timestamp: number;
  status: SimulationStatus;
  currentTick: number;
  totalTicks: number;
  currentPrice: number;
  priceChange: number;
  priceChangePct: number;
  priceHistory: PricePoint[];
  circuitBreaker: boolean;
  sentiment: {
    bullish: number;
    neutral: number;
    bearish: number;
  };
  predictions: Predictions;
  totalAgents: number;
}

export interface NewsItem {
  id: string;
  headline: string;
  sentiment: SentimentType;
  impactScore: number; // 1-10
  affected_sectors?: string[];
  source: string;
  timestamp: string;
  historical_parallel?: string | null;
}

export interface AgentAction {
  agent_id: string;
  agent_type: string;
  action: 'BUY' | 'SELL' | 'HOLD';
  quantity: number;
  price_target: number;
  reasoning: string;
  timestamp: string;
}

export interface CascadeNode {
  id: string;
  label: string;
  type: 'target' | 'supplier' | 'competitor' | 'etf' | 'macro';
  impactScore: number;
  direction: 'positive' | 'negative' | 'neutral';
}
