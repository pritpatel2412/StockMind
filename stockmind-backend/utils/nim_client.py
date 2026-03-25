"""
NIM Client
NVIDIA NIM wrapper for embeddings and vector operations
"""

from typing import List, Dict, Any, Optional
import httpx

from config import NIM_API_KEY, NIM_BASE_URL, NIM_EMBEDDINGS_MODEL


class NIMClient:
    """
    Wrapper for NVIDIA NIM embeddings API.
    Handles async requests to NIM service for semantic search.
    """
    
    def __init__(
        self,
        api_key: str = NIM_API_KEY,
        base_url: str = NIM_BASE_URL,
    ):
        """
        Initialize NIM client.
        
        Args:
            api_key: NIM API key
            base_url: NIM service base URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = NIM_EMBEDDINGS_MODEL
        self.http_client: Optional[httpx.AsyncClient] = None
    
    async def initialize(self) -> None:
        """Initialize async HTTP client."""
        headers = {}
        if self.api_key and self.api_key != "your_nim_api_key_here":
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        self.http_client = httpx.AsyncClient(timeout=30.0, headers=headers)
    
    async def close(self) -> None:
        """Close HTTP client."""
        if self.http_client:
            await self.http_client.aclose()
    
    async def embed(self, text: str) -> Optional[List[float]]:
        """
        Create embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector or None on failure
        """
        if not self.http_client:
            await self.initialize()
        
        try:
            response = await self.http_client.post(
                f"{self.base_url}/embeddings",
                json={
                    "model": self.model,
                    "input": text,
                },
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["data"][0]["embedding"]
        
        except Exception as e:
            print(f"[NIM] Error embedding text: {e}")
        
        return None
    
    async def embed_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """
        Embed multiple texts efficiently.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings (None if failed)
        """
        if not self.http_client:
            await self.initialize()
        
        try:
            response = await self.http_client.post(
                f"{self.base_url}/embeddings",
                json={
                    "model": self.model,
                    "input": texts,
                },
            )
            
            if response.status_code == 200:
                data = response.json()
                # Return embeddings in order
                embeddings = sorted(data["data"], key=lambda x: x["index"])
                return [emb["embedding"] for emb in embeddings]
        
        except Exception as e:
            print(f"[NIM] Error embedding batch: {e}")
        
        return [None] * len(texts)
