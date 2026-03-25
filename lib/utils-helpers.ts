import clsx from 'clsx';

export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}

// Sentiment color mapping
export const SENTIMENT_COLORS = {
  bullish: '#00ff88',      // Neon green
  neutral: '#00aaff',      // Electric blue
  bearish: '#ff1744',      // Red
} as const;

export const SENTIMENT_TAILWIND = {
  bullish: 'text-[#00ff88]',
  neutral: 'text-[#00aaff]',
  bearish: 'text-[#ff1744]',
} as const;

export const SENTIMENT_BG_TAILWIND = {
  bullish: 'bg-[#00ff8811] border-[#00ff88]',
  neutral: 'bg-[#00aaff11] border-[#00aaff]',
  bearish: 'bg-[#ff174411] border-[#ff1744]',
} as const;

// Format currency
export function formatCurrency(value: number, decimals = 2): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

// Format percentage
export function formatPercent(value: number, decimals = 2): string {
  const sign = value >= 0 ? '+' : '';
  return `${sign}${value.toFixed(decimals)}%`;
}

// Get color for percentage
export function getPercentColor(value: number): string {
  if (value > 0) return SENTIMENT_COLORS.bullish;
  if (value < 0) return SENTIMENT_COLORS.bearish;
  return SENTIMENT_COLORS.neutral;
}

export function getPercentTailwind(value: number): string {
  if (value > 0) return 'text-[#00ff88]';
  if (value < 0) return 'text-[#ff1744]';
  return 'text-[#00aaff]';
}

// Format large numbers
export function formatNumber(value: number, decimals = 0): string {
  const absValue = Math.abs(value);
  if (absValue >= 1000000) {
    return `${(value / 1000000).toFixed(decimals)}M`;
  }
  if (absValue >= 1000) {
    return `${(value / 1000).toFixed(decimals)}K`;
  }
  return value.toFixed(decimals);
}

// Format time
export function formatTime(timestamp: number): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
}

// Format date
export function formatDate(timestamp: number): string {
  const date = new Date(timestamp);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

// Calculate percentage change
export function calculatePercentChange(from: number, to: number): number {
  return ((to - from) / from) * 100;
}

// Truncate text
export function truncate(text: string, length: number): string {
  return text.length > length ? text.substring(0, length) + '...' : text;
}
