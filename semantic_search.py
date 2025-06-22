"""
Semantic Search - Finds most relevant chunks using embeddings
"""
import os
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import openai
import json


def _cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
        
    return dot_product / (norm_v1 * norm_v2)


class SemanticSearcher:
    """Handles semantic search using OpenAI embeddings"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize semantic searcher
        
        Args:
            openai_api_key: OpenAI API key (if not provided, looks for OPENAI_API_KEY env var)
        """
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it directly.")
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)
        self.embedding_model = "text-embedding-3-small"  # More cost-effective than ada-002
        
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for a text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return []
    
    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for multiple texts in batch
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"Error getting batch embeddings: {e}")
            return []
    
    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add embeddings to chunks
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            Chunks with embeddings added
        """
        # Prepare texts for embedding
        texts = []
        for chunk in chunks:
            # Combine title and content for better context
            text = f"{chunk.get('title', '')}\n\n{chunk.get('content', '')}"
            texts.append(text.strip())
        
        # Get embeddings in batch
        embeddings = self.get_embeddings_batch(texts)
        
        # Add embeddings to chunks
        for i, chunk in enumerate(chunks):
            if i < len(embeddings):
                chunk['embedding'] = embeddings[i]
            else:
                chunk['embedding'] = []
        
        return chunks
    
    def find_relevant_chunks(
        self, 
        query: str, 
        chunks: List[Dict[str, Any]], 
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Find most relevant chunks for a query
        
        Args:
            query: Search query
            chunks: List of chunks with embeddings
            top_k: Number of top chunks to return
            
        Returns:
            List of most relevant chunks with similarity scores
        """
        # Get query embedding
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return []
        
        query_vector = np.array(query_embedding)
        
        # Calculate similarities
        similarities = []
        for chunk in chunks:
            chunk_embedding = chunk.get('embedding', [])
            if chunk_embedding:
                chunk_vector = np.array(chunk_embedding)
                similarity = _cosine_similarity(query_vector, chunk_vector)
                similarities.append((chunk, similarity))
        
        # Sort by similarity and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        relevant_chunks = []
        for chunk, score in similarities[:top_k]:
            relevant_chunk = chunk.copy()
            relevant_chunk['similarity_score'] = float(score)
            # Remove embedding from response to reduce size
            relevant_chunk.pop('embedding', None)
            relevant_chunks.append(relevant_chunk)
        
        return relevant_chunks
    
    def search_with_fallback(
        self, 
        query: str, 
        chunks: List[Dict[str, Any]], 
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search with keyword fallback if semantic search fails
        
        Args:
            query: Search query
            chunks: List of chunks
            top_k: Number of top chunks to return
            
        Returns:
            List of most relevant chunks
        """
        try:
            return self.find_relevant_chunks(query, chunks, top_k)
        except Exception as e:
            print(f"Semantic search failed: {e}")
            return self._keyword_fallback(query, chunks, top_k)
    
    def _keyword_fallback(
        self, 
        query: str, 
        chunks: List[Dict[str, Any]], 
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Fallback keyword-based search
        
        Args:
            query: Search query
            chunks: List of chunks
            top_k: Number of top chunks to return
            
        Returns:
            List of chunks ranked by keyword relevance
        """
        query_words = set(query.lower().split())
        
        scored_chunks = []
        for chunk in chunks:
            content = f"{chunk.get('title', '')} {chunk.get('content', '')}".lower()
            content_words = set(content.split())
            
            # Simple keyword matching score
            common_words = query_words.intersection(content_words)
            score = len(common_words) / len(query_words) if query_words else 0
            
            if score > 0:
                result_chunk = chunk.copy()
                result_chunk['similarity_score'] = score
                result_chunk['search_type'] = 'keyword_fallback'
                # Remove embedding to reduce response size
                result_chunk.pop('embedding', None)
                scored_chunks.append(result_chunk)
        
        # Sort by score and return top-k
        scored_chunks.sort(key=lambda x: x['similarity_score'], reverse=True)
        return scored_chunks[:top_k]
