"""
Market Data Fetcher
Integrates yfinance for price data and manages order book calculations
"""

from typing import List, Tuple, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import yfinance as yf
import math

from models.schemas import OrderBook, TickUpdate
from config import INITIAL_PRICE, INITIAL_VOLUME


class MarketFetcher:
    """
    Fetches real market data from yfinance and provides price calculations
    for order book aggregation.
    """
    
    def __init__(self, ticker: str = "AAPL"):
        """
        Initialize market fetcher.
        
        Args:
            ticker: Stock ticker symbol (default: AAPL)
        """
        self.ticker = ticker
        self.last_fetch = None
    
    async def fetch_historical_data(
        self,
        period: str = "1mo",
        interval: str = "1d",
    ) -> Dict[str, Any]:
        """
        Fetch historical price data from yfinance.
        
        Args:
            period: Time period ('1mo', '3mo', '1y', etc.)
            interval: Data interval ('1m', '5m', '1h', '1d', etc.)
            
        Returns:
            Dictionary with OHLCV data
        """
        try:
            data = yf.download(
                self.ticker,
                period=period,
                interval=interval,
                progress=False,
            )
            self.last_fetch = datetime.now()
            return data.to_dict()
        except Exception as e:
            print(f"[Market Fetcher] Error fetching {self.ticker}: {e}")
            return {}
    
    async def get_current_price(self) -> float:
        """Get latest price for ticker."""
        try:
            ticker = yf.Ticker(self.ticker)
            data = ticker.history(period="1d")
            if len(data) > 0:
                return float(data['Close'].iloc[-1])
        except Exception as e:
            print(f"[Market Fetcher] Error getting current price: {e}")
        
        return INITIAL_PRICE
    
    @staticmethod
    def calculate_price_from_orders(
        buy_orders: List[Tuple[float, int]],
        sell_orders: List[Tuple[float, int]],
    ) -> float:
        """
        Calculate market price from buy/sell orders using supply/demand.
        
        Uses VWAP (volume-weighted average price) concept:
        - Buy orders move price down (negative demand)
        - Sell orders move price up (negative supply)
        
        Args:
            buy_orders: [(price, quantity), ...]
            sell_orders: [(price, quantity), ...]
            
        Returns:
            Aggregated market price
        """
        if not buy_orders and not sell_orders:
            return INITIAL_PRICE
        
        # Calculate demand (buy) and supply (sell) pressure
        buy_volume = sum(qty for _, qty in buy_orders)
        buy_price = sum(price * qty for price, qty in buy_orders) / buy_volume if buy_volume > 0 else INITIAL_PRICE
        
        sell_volume = sum(qty for _, qty in sell_orders)
        sell_price = sum(price * qty for price, qty in sell_orders) / sell_volume if sell_volume > 0 else INITIAL_PRICE
        
        # Weight by relative volumes
        total_volume = buy_volume + sell_volume
        if total_volume == 0:
            return INITIAL_PRICE
        
        buy_weight = buy_volume / total_volume
        sell_weight = sell_volume / total_volume
        
        # Price pressure: buyers push up, sellers push down
        equilibrium_price = (buy_price * buy_weight + sell_price * sell_weight)
        return equilibrium_price
    
    @staticmethod
    def calculate_volatility(
        prices: List[float],
        lookback: int = 20,
    ) -> float:
        """
        Calculate historical volatility (standard deviation of returns).
        
        Args:
            prices: List of prices
            lookback: Number of periods for calculation
            
        Returns:
            Volatility as decimal (0.02 = 2%)
        """
        if len(prices) < 2:
            return 0.02
        
        recent_prices = prices[-lookback:] if len(prices) >= lookback else prices
        
        # Calculate returns
        returns = [
            (recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1]
            for i in range(1, len(recent_prices))
        ]
        
        if not returns:
            return 0.02
        
        # Calculate standard deviation
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        volatility = math.sqrt(variance)
        
        # Clamp to reasonable bounds
        return max(0.001, min(0.50, volatility))
    
    @staticmethod
    def create_order_book(
        mid_price: float,
        spread: float,
        depth: int = 10,
    ) -> OrderBook:
        """
        Create synthetic order book around mid price.
        
        Args:
            mid_price: Center price
            spread: Bid-ask spread
            depth: Number of levels on each side
            
        Returns:
            OrderBook with bids and asks
        """
        bids = []
        asks = []
        
        bid_base = mid_price - spread / 2
        ask_base = mid_price + spread / 2
        
        # Generate bid side (decreasing prices)
        for i in range(depth):
            price = bid_base - (i * 0.05)
            # Quantity decreases as we go further from mid
            quantity = int(INITIAL_VOLUME * (0.5 ** (i / 5)))
            bids.append((price, quantity))
        
        # Generate ask side (increasing prices)
        for i in range(depth):
            price = ask_base + (i * 0.05)
            quantity = int(INITIAL_VOLUME * (0.5 ** (i / 5)))
            asks.append((price, quantity))
        
        return OrderBook(
            bids=bids,
            asks=asks,
            spread=spread,
            mid_price=mid_price,
        )
    
    @staticmethod
    def calculate_vwap(
        trades: List[Tuple[float, int]],
    ) -> float:
        """
        Calculate volume-weighted average price.
        
        Args:
            trades: [(price, quantity), ...]
            
        Returns:
            VWAP
        """
        if not trades:
            return INITIAL_PRICE
        
        total_value = sum(price * qty for price, qty in trades)
        total_volume = sum(qty for _, qty in trades)
        
        if total_volume == 0:
            return INITIAL_PRICE
        
        return total_value / total_volume
