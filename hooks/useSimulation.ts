'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { SimulationData } from '@/lib/types';

type ConnectionStatus = 'disconnected' | 'connecting' | 'connected' | 'error';

export function useSimulation(simulationId: string | null) {
  const [data, setData] = useState<SimulationData | null>(null);
  const [status, setStatus] = useState<ConnectionStatus>('disconnected');
  const [error, setError] = useState<string | null>(null);
  const ws = useRef<WebSocket | null>(null);
  const reconnectCount = useRef(0);
  const maxRetries = 5;

  const connect = useCallback(() => {
    if (!simulationId) return;

    setStatus('connecting');
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
    try {
      ws.current = new WebSocket(`${wsUrl}/ws/${simulationId}`);

      ws.current.onopen = () => {
        setStatus('connected');
        reconnectCount.current = 0;
        setError(null);
      };

      ws.current.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          setData(parsed as SimulationData);
        } catch (e) {
          console.error("Failed to parse websocket message", e);
        }
      };

      ws.current.onclose = () => {
        setStatus('disconnected');
        if (reconnectCount.current < maxRetries) {
          reconnectCount.current += 1;
          const backoff = Math.min(1000 * Math.pow(2, reconnectCount.current), 10000);
          setTimeout(() => connect(), backoff);
        } else {
          setError('Max reconnection attempts reached.');
          setStatus('error');
        }
      };

      ws.current.onerror = () => {
        setError('WebSocket encountered an error.');
        setStatus('error');
      };
    } catch (e: any) {
      setError(e.message);
      setStatus('error');
    }
  }, [simulationId]);

  useEffect(() => {
    if (simulationId) {
      connect();
    } else {
      if (ws.current) {
        ws.current.close();
      }
      setData(null);
      setStatus('disconnected');
    }

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [simulationId, connect]);

  const disconnect = useCallback(() => {
    reconnectCount.current = maxRetries; // Prevent auto-reconnect
    if (ws.current) {
      ws.current.close();
    }
    setData(null);
    setStatus('disconnected');
  }, []);

  return { data, status, error, disconnect };
}
