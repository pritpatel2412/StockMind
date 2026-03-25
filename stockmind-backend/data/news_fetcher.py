"""
News Data Fetcher
Integrates NewsAPI and mock data for sentiment analysis
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
import asyncio

from models.schemas import NewsItem, SentimentType
from config import NEWS_API_KEY


class NewsFetcher:
    """
    Fetches financial news and provides sentiment analysis.
    Uses NewsAPI for real data, with mock fallback.
    """
    
    def __init__(self, api_key: str = NEWS_API_KEY):
        """
        Initialize news fetcher.
        
        Args:
            api_key: NewsAPI API key
        """
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
        self.http_client = None
    
    async def initialize(self) -> None:
        """Initialize async HTTP client."""
        self.http_client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self) -> None:
        """Close HTTP client."""
        if self.http_client:
            await self.http_client.aclose()
    
    async def fetch_news(
        self,
        query: str = "stock market",
        country: str = "us",
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Fetch news headlines from NewsAPI.
        
        Args:
            query: Search query
            country: Country code (us, gb, etc.)
            limit: Number of articles
            
        Returns:
            List of news articles or mock data if API fails
        """
        if not self.api_key or self.api_key == "your_newsapi_key_here":
            return self._get_mock_news()
        
        try:
            if not self.http_client:
                await self.initialize()
            
            # Try NewsAPI
            url = f"{self.base_url}/top-headlines"
            params = {
                "category": "business",
                "country": country,
                "apiKey": self.api_key,
                "pageSize": limit,
            }
            
            response = await self.http_client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get("articles", [])
        
        except Exception as e:
            print(f"[News Fetcher] Error fetching news: {e}")
        
        # Fallback to mock data
        return self._get_mock_news()
    
    async def classify_sentiment(
        self,
        headlines: List[str],
    ) -> List[tuple[str, SentimentType]]:
        """
        Classify sentiment of headlines using keyword heuristics.
        In production, would use LLM via Groq for better accuracy.
        
        Args:
            headlines: List of headline texts
            
        Returns:
            List of (headline, sentiment) tuples
        """
        bullish_keywords = [
            "surge", "rally", "jump", "gain", "beat", "profit", "strong",
            "success", "growth", "up", "bull", "boom", "record", "peak"
        ]
        bearish_keywords = [
            "crash", "plunge", "fall", "drop", "loss", "miss", "weak",
            "decline", "fail", "down", "bear", "bust", "slump", "worst"
        ]
        
        results = []
        
        for headline in headlines:
            headline_lower = headline.lower()
            
            bullish_score = sum(
                1 for keyword in bullish_keywords 
                if keyword in headline_lower
            )
            bearish_score = sum(
                1 for keyword in bearish_keywords 
                if keyword in headline_lower
            )
            
            if bullish_score > bearish_score:
                sentiment = SentimentType.BULLISH
            elif bearish_score > bullish_score:
                sentiment = SentimentType.BEARISH
            else:
                sentiment = SentimentType.NEUTRAL
            
            results.append((headline, sentiment))
        
        return results
    
    def _get_mock_news(self) -> List[Dict[str, Any]]:
        """Return mock news for testing."""
        return [
            {
                "title": "Stock Market Surges on Strong Earnings Reports",
                "description": "Major tech stocks rally following better-than-expected Q3 results",
                "url": "https://example.com/news1",
                "source": {"name": "Financial Times"},
                "publishedAt": datetime.now().isoformat(),
            },
            {
                "title": "Fed Signals Potential Rate Cuts in 2024",
                "description": "Federal Reserve chair hints at possible interest rate reductions",
                "url": "https://example.com/news2",
                "source": {"name": "Reuters"},
                "publishedAt": datetime.now().isoformat(),
            },
            {
                "title": "Tech Sector Faces Regulatory Scrutiny",
                "description": "New regulations could impact major technology companies",
                "url": "https://example.com/news3",
                "source": {"name": "Wall Street Journal"},
                "publishedAt": datetime.now().isoformat(),
            },
            {
                "title": "Bitcoin Plunges Amid Macroeconomic Concerns",
                "description": "Cryptocurrency markets experience significant volatility",
                "url": "https://example.com/news4",
                "source": {"name": "CoinDesk"},
                "publishedAt": datetime.now().isoformat(),
            },
            {
                "title": "Healthcare Stocks Rally on Drug Approvals",
                "description": "Pharma companies surge following FDA approvals",
                "url": "https://example.com/news5",
                "source": {"name": "Healthcare Weekly"},
                "publishedAt": datetime.now().isoformat(),
            },
        ]
    
    async def create_news_items(
        self,
        articles: List[Dict[str, Any]],
    ) -> List[NewsItem]:
        """
        Convert raw articles to NewsItem objects with sentiment.
        
        Args:
            articles: Raw articles from NewsAPI
            
        Returns:
            List of NewsItem with sentiment classification
        """
        headlines = [
            article.get("title", "")
            for article in articles
            if article.get("title")
        ]
        
        if not headlines:
            return []
        
        # Classify sentiments
        sentiment_classifications = await self.classify_sentiment(headlines)
        
        news_items = []
        for article, (_, sentiment) in zip(articles, sentiment_classifications):
            # Determine impact score based on sentiment intensity
            impact_scores = {
                SentimentType.EXTREME_BULLISH: 0.95,
                SentimentType.BULLISH: 0.7,
                SentimentType.NEUTRAL: 0.3,
                SentimentType.BEARISH: 0.7,
                SentimentType.EXTREME_BEARISH: 0.95,
            }
            
            news_item = NewsItem(
                title=article.get("title", "Unknown"),
                source=article.get("source", {}).get("name", "Unknown"),
                url=article.get("url", ""),
                sentiment=sentiment,
                confidence=0.7 if sentiment == SentimentType.NEUTRAL else 0.85,
                impact_score=impact_scores.get(sentiment, 0.5),
                published_at=datetime.fromisoformat(
                    article.get("publishedAt", datetime.now().isoformat())
                ),
                summary=article.get("description", ""),
            )
            news_items.append(news_item)
        
        return news_items
