"""
FastAPI Web Content Parser and QA Assistant (Simplified Version)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import traceback
import time

from html_parser import HTMLParser
from content_chunker import ContentChunker
from semantic_search_simple import SemanticSearcher


app = FastAPI(
    title="Web Content Parser & QA Assistant",
    description="Extract, chunk, and search web content with semantic understanding",
    version="1.0.0"
)


# Request/Response Models
class ProcessRequest(BaseModel):
    html: str = Field(..., description="Raw HTML content from document.body.innerHTML")
    query: str = Field(..., description="User query for content extraction or modification")
    chunk_size: Optional[int] = Field(750, description="Target chunk size in tokens", ge=100, le=2000)
    top_k: Optional[int] = Field(3, description="Number of most relevant chunks to return", ge=1, le=10)


class ChunkResponse(BaseModel):
    id: str
    title: str
    content: str
    token_count: int
    type: str


class RelevantChunkResponse(BaseModel):
    id: str
    title: str
    content: str
    similarity_score: float
    token_count: int
    type: str


class ProcessResponse(BaseModel):
    success: bool
    title: str
    clean_markdown: str
    chunks: List[ChunkResponse]
    most_relevant_chunks: List[RelevantChunkResponse]
    processing_time: float
    metadata: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: float


# Global instances
html_parser = HTMLParser()
content_chunker = ContentChunker()
semantic_searcher = None  # Initialize when needed


def get_semantic_searcher():
    """Lazy initialization of semantic searcher"""
    global semantic_searcher
    if semantic_searcher is None:
        try:
            semantic_searcher = SemanticSearcher()
        except ValueError as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Semantic search unavailable: {str(e)}"
            )
    return semantic_searcher


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Web Content Parser & QA Assistant is running",
        timestamp=time.time()
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    """Detailed health check"""
    return HealthResponse(
        status="healthy",
        message="All systems operational",
        timestamp=time.time()
    )


@app.post("/process", response_model=ProcessResponse)
async def process_content(request: ProcessRequest):
    """
    Main endpoint to process HTML content and find relevant chunks
    
    Args:
        request: ProcessRequest containing HTML and query
        
    Returns:
        ProcessResponse with cleaned markdown, chunks, and relevant chunks
    """
    start_time = time.time()
    
    try:
        # Step 1: Parse HTML and extract clean content
        parse_result = html_parser.extract_main_content(request.html)
        
        if not parse_result["success"]:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse HTML: {parse_result.get('error', 'Unknown error')}"
            )
        
        title = parse_result["title"]
        clean_markdown = parse_result["markdown"]
        
        if not clean_markdown.strip():
            raise HTTPException(
                status_code=400,
                detail="No meaningful content could be extracted from the HTML"
            )
        
        # Step 2: Initialize chunker with custom size if provided
        if request.chunk_size != 750:
            chunker = ContentChunker(target_chunk_size=request.chunk_size)
        else:
            chunker = content_chunker
        
        # Step 3: Create chunks
        chunks = chunker.chunk_by_headings(clean_markdown, title)
        
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Could not create meaningful chunks from the content"
            )
        
        # Step 4: Find relevant chunks using semantic search
        try:
            searcher = get_semantic_searcher()
            
            # Add embeddings to chunks
            chunks_with_embeddings = searcher.embed_chunks(chunks)
            
            # Find most relevant chunks
            relevant_chunks = searcher.search_with_fallback(
                request.query, 
                chunks_with_embeddings, 
                request.top_k
            )
            
        except Exception as e:
            # Fallback to keyword search if semantic search fails
            print(f"Semantic search failed: {e}")
            relevant_chunks = _keyword_fallback_search(request.query, chunks, request.top_k)
        
        # Step 5: Prepare response
        processing_time = time.time() - start_time
        
        # Convert chunks to response format (remove embeddings)
        clean_chunks = []
        for chunk in chunks:
            clean_chunks.append(ChunkResponse(
                id=chunk["id"],
                title=chunk["title"],
                content=chunk["content"],
                token_count=chunk["token_count"],
                type=chunk["type"]
            ))
        
        # Convert relevant chunks to response format
        relevant_chunk_responses = []
        for chunk in relevant_chunks:
            relevant_chunk_responses.append(RelevantChunkResponse(
                id=chunk["id"],
                title=chunk["title"],
                content=chunk["content"],
                similarity_score=chunk.get("similarity_score", 0.0),
                token_count=chunk["token_count"],
                type=chunk["type"]
            ))
        
        return ProcessResponse(
            success=True,
            title=title,
            clean_markdown=clean_markdown,
            chunks=clean_chunks,
            most_relevant_chunks=relevant_chunk_responses,
            processing_time=processing_time,
            metadata={
                "total_chunks": len(chunks),
                "original_html_length": len(request.html),
                "markdown_length": len(clean_markdown),
                "fallback_used": parse_result.get("fallback", False),
                "search_type": "semantic"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


def _keyword_fallback_search(query: str, chunks: List[Dict], top_k: int) -> List[Dict]:
    """Simple keyword-based search fallback"""
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
            scored_chunks.append(result_chunk)
    
    # Sort by score and return top-k
    scored_chunks.sort(key=lambda x: x['similarity_score'], reverse=True)
    return scored_chunks[:top_k]


@app.post("/parse-only")
async def parse_html_only(html: str):
    """
    Parse HTML only without chunking or semantic search
    
    Args:
        html: Raw HTML content
        
    Returns:
        Parsed content with title and markdown
    """
    try:
        parse_result = html_parser.extract_main_content(html)
        
        if not parse_result["success"]:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse HTML: {parse_result.get('error', 'Unknown error')}"
            )
        
        return {
            "success": True,
            "title": parse_result["title"],
            "clean_markdown": parse_result["markdown"],
            "fallback_used": parse_result.get("fallback", False)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Parse-only error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 