"""
Groq API Client
LLM wrapper with rate limiting, retry logic, and structured JSON outputs
"""

from typing import Optional, Dict, Any
import asyncio
import httpx
from datetime import datetime, timedelta
import json

from config import GROQ_API_KEY, GROQ_RATE_LIMIT, GROQ_RATE_WINDOW


class RateLimiter:
    """Token bucket rate limiter for API calls."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Max requests per window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: list[datetime] = []
    
    async def wait_if_needed(self) -> None:
        """Wait if rate limit would be exceeded."""
        now = datetime.now()
        # Remove old requests outside window
        self.requests = [
            req_time for req_time in self.requests
            if (now - req_time).total_seconds() < self.window_seconds
        ]
        
        if len(self.requests) >= self.max_requests:
            # Calculate wait time until oldest request leaves window
            wait_until = self.requests[0] + timedelta(seconds=self.window_seconds)
            wait_seconds = (wait_until - now).total_seconds()
            if wait_seconds > 0:
                await asyncio.sleep(wait_seconds)
        
        self.requests.append(now)


class GroqClient:
    """
    Groq API client with rate limiting, retry logic, and JSON parsing.
    Uses llama-3.3-70b for fast inference.
    """
    
    def __init__(self, api_key: str = GROQ_API_KEY):
        """
        Initialize Groq client.
        
        Args:
            api_key: Groq API key
        """
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "llama-3.3-70b-versatile"
        self.rate_limiter = RateLimiter(GROQ_RATE_LIMIT, GROQ_RATE_WINDOW)
        self.http_client: Optional[httpx.AsyncClient] = None
    
    async def initialize(self) -> None:
        """Initialize async HTTP client."""
        self.http_client = httpx.AsyncClient(timeout=60.0)
    
    async def close(self) -> None:
        """Close HTTP client."""
        if self.http_client:
            await self.http_client.aclose()
    
    async def create_chat_completion(
        self,
        messages: list[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500,
        json_mode: bool = False,
        retries: int = 3,
    ) -> Optional[str]:
        """
        Create chat completion via Groq API.
        
        Args:
            messages: Chat messages (role/content format)
            temperature: Sampling temperature
            max_tokens: Max response tokens
            json_mode: Force JSON output format
            retries: Number of retries on failure
            
        Returns:
            Response text or None on failure
        """
        if not self.api_key or self.api_key == "your_groq_api_key_here":
            return self._get_mock_response(messages, json_mode)
        
        await self.rate_limiter.wait_if_needed()
        
        if not self.http_client:
            await self.initialize()
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        for attempt in range(retries):
            try:
                response = await self.http_client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                elif response.status_code == 429:  # Rate limited
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"[Groq] Error: {response.status_code} - {response.text}")
                    return None
            
            except Exception as e:
                print(f"[Groq] Exception: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(1)
        
        return None
    
    async def analyze_sentiment(self, headline: str) -> Dict[str, Any]:
        """
        Analyze sentiment of headline.
        
        Args:
            headline: News headline
            
        Returns:
            Dict with sentiment and confidence
        """
        from config import SENTIMENT_ANALYSIS_PROMPT
        
        prompt = SENTIMENT_ANALYSIS_PROMPT.format(headline=headline)
        
        messages = [
            {
                "role": "system",
                "content": "You are a financial sentiment analyst. Respond with JSON only.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]
        
        response = await self.create_chat_completion(
            messages,
            temperature=0.3,
            max_tokens=100,
            json_mode=True,
        )
        
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        return {"sentiment": "neutral", "confidence": 0.5}
    
    async def make_trading_decision(
        self,
        agent_type: str,
        price: float,
        volatility: float,
        bid: float,
        ask: float,
        recent_volume: int,
        sentiment: str,
        recent_news: str,
        historical_context: str,
        agent_suffix: str,
    ) -> Dict[str, Any]:
        """
        Make trading decision for agent.
        
        Args:
            agent_type: Type of agent
            price: Current price
            volatility: Current volatility
            bid: Best bid
            ask: Best ask
            recent_volume: Recent volume
            sentiment: Market sentiment
            recent_news: Recent news context
            historical_context: Historical similar events
            agent_suffix: Agent-specific decision instructions
            
        Returns:
            Dict with action, size, and reasoning
        """
        from config import DECISION_PROMPT_TEMPLATE
        
        prompt = DECISION_PROMPT_TEMPLATE.format(
            agent_type=agent_type,
            price=price,
            volatility=volatility,
            bid=bid,
            ask=ask,
            volume=recent_volume,
            sentiment=sentiment,
            recent_events=recent_news,
            historical_context=historical_context,
            agent_suffix=agent_suffix,
        )
        
        messages = [
            {
                "role": "system",
                "content": "You are a financial agent making trading decisions. Respond with JSON only.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]
        
        response = await self.create_chat_completion(
            messages,
            temperature=0.7,
            max_tokens=200,
            json_mode=True,
        )
        
        if response:
            try:
                res_json = json.loads(response)
                print(f"[LLM] {agent_type} DECISION: {res_json.get('action', 'HOLD')} | Size: {res_json.get('size', 0)} | Reasoning: {res_json.get('reasoning', '')[:50]}...")
                return res_json
            except json.JSONDecodeError:
                pass
        
        return {"action": "hold", "size": 0, "reasoning": "Unable to decide"}
    
    def _get_mock_response(
        self,
        messages: list[Dict[str, str]],
        json_mode: bool = False,
    ) -> str:
        """Return mock response for testing."""
        if json_mode:
            return json.dumps({
                "action": "hold",
                "size": 0,
                "reasoning": "Mock response",
            })
        return "Mock response from Groq"
