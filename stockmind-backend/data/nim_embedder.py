"""
NVIDIA NIM Embeddings and Vector Search
Semantic search for historical events RAG
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from datetime import datetime

from config import HISTORICAL_EVENTS, NIM_EMBEDDINGS_MODEL


class NIMEmbedder:
    """
    Embeddings and semantic search using NVIDIA NIM.
    For MVP, uses simple TF-IDF-like similarity.
    In production, would call NIM API for neural embeddings.
    """
    
    def __init__(self):
        """Initialize embedder with pre-loaded historical events."""
        self.historical_events = HISTORICAL_EVENTS
        self.embeddings: Dict[str, np.ndarray] = {}
        self._initialize_vectors()
    
    def _initialize_vectors(self) -> None:
        """Initialize simple word-based vectors for MVP."""
        # For MVP: use simple bag-of-words similarity
        # In production: would call NIM API
        pass
    
    async def embed_text(self, text: str) -> List[float]:
        """
        Embed text to vector (mock implementation).
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        # MVP: return simple keyword features
        keywords = ["volatility", "crash", "rally", "sentiment", "bearish", "bullish"]
        vector = []
        text_lower = text.lower()
        
        for keyword in keywords:
            vector.append(1.0 if keyword in text_lower else 0.0)
        
        return vector
    
    async def semantic_search(
        self,
        query: str,
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Find most similar historical events to query.
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            List of similar historical events with similarity scores
        """
        query_vector = await self.embed_text(query)
        
        results = []
        for event in self.historical_events:
            event_text = f"{event['title']} {event['description']}"
            event_vector = await self.embed_text(event_text)
            
            # Simple cosine similarity
            similarity = self._cosine_similarity(query_vector, event_vector)
            
            results.append({
                "title": event["title"],
                "description": event["description"],
                "impact": event.get("impact", "neutral"),
                "volatility_spike": event.get("volatility_spike", 0.1),
                "similarity_score": float(similarity),
            })
        
        # Sort by similarity and return top-k
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]
    
    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            return 0.0
        
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    async def format_rag_context(
        self,
        query: str,
        top_k: int = 3,
    ) -> str:
        """
        Get similar historical events formatted for LLM context.
        
        Args:
            query: Decision query
            top_k: Number of events to include
            
        Returns:
            Formatted RAG context string
        """
        similar_events = await self.semantic_search(query, top_k)
        
        if not similar_events:
            return "No similar historical events found."
        
        context_lines = ["## Similar Historical Events:"]
        
        for i, event in enumerate(similar_events, 1):
            context_lines.append(
                f"\n{i}. {event['title']} (Similarity: {event['similarity_score']:.2%})"
            )
            context_lines.append(f"   Description: {event['description']}")
            context_lines.append(f"   Impact: {event['impact']}")
            context_lines.append(
                f"   Volatility Spike: {event['volatility_spike']:.0%}"
            )
        
        return "\n".join(context_lines)
