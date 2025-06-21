"""
Content Chunker - Splits content into semantic chunks
"""
import re
import tiktoken
from typing import List, Dict, Any, Optional


class ContentChunker:
    """Splits markdown content into semantic chunks"""
    
    def __init__(self, target_chunk_size: int = 750, overlap_percentage: float = 0.15):
        """
        Initialize chunker
        
        Args:
            target_chunk_size: Target size in tokens for each chunk
            overlap_percentage: Percentage of overlap between chunks (0.0 - 1.0)
        """
        self.target_chunk_size = target_chunk_size
        self.overlap_tokens = int(target_chunk_size * overlap_percentage)
        self.encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
        
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    def chunk_by_headings(self, markdown: str, title: str = "") -> List[Dict[str, Any]]:
        """
        Split markdown by headings first, then by size if needed
        
        Args:
            markdown: Markdown content to chunk
            title: Document title
            
        Returns:
            List of chunks with metadata
        """
        chunks = []
        
        # Split by headings (##, ###, etc.)
        sections = self._split_by_headings(markdown)
        
        chunk_id = 1
        for section in sections:
            section_title = section.get("title", f"Section {chunk_id}")
            section_content = section.get("content", "")
            
            # If section is small enough, use as-is
            if self.count_tokens(section_content) <= self.target_chunk_size:
                chunks.append({
                    "id": str(chunk_id),
                    "title": section_title,
                    "content": section_content.strip(),
                    "token_count": self.count_tokens(section_content),
                    "type": "heading_based"
                })
                chunk_id += 1
            else:
                # Split large sections into smaller chunks
                sub_chunks = self._split_by_size(section_content, section_title)
                for i, sub_chunk in enumerate(sub_chunks):
                    chunks.append({
                        "id": str(chunk_id),
                        "title": f"{section_title} (Part {i+1})",
                        "content": sub_chunk.strip(),
                        "token_count": self.count_tokens(sub_chunk),
                        "type": "size_based"
                    })
                    chunk_id += 1
        
        # If no meaningful chunks were created, fall back to size-based chunking
        if not chunks:
            chunks = self.chunk_by_size(markdown, title)
        
        return chunks
    
    def chunk_by_size(self, markdown: str, title: str = "") -> List[Dict[str, Any]]:
        """
        Split markdown by fixed token size with overlap
        
        Args:
            markdown: Markdown content to chunk
            title: Document title
            
        Returns:
            List of chunks with metadata
        """
        chunks = []
        text_chunks = self._split_by_size(markdown)
        
        for i, chunk_content in enumerate(text_chunks):
            chunks.append({
                "id": str(i + 1),
                "title": f"{title} - Chunk {i + 1}" if title else f"Chunk {i + 1}",
                "content": chunk_content.strip(),
                "token_count": self.count_tokens(chunk_content),
                "type": "size_based"
            })
        
        return chunks
    
    def _split_by_headings(self, markdown: str) -> List[Dict[str, str]]:
        """Split markdown content by headings"""
        sections = []
        
        # Find all headings
        heading_pattern = r'^(#{1,6})\s+(.+)$'
        lines = markdown.split('\n')
        
        current_section = {"title": "", "content": "", "level": 0}
        
        for line in lines:
            match = re.match(heading_pattern, line, re.MULTILINE)
            
            if match:
                # Save previous section if it has content
                if current_section["content"].strip():
                    sections.append(current_section.copy())
                
                # Start new section
                heading_level = len(match.group(1))
                heading_text = match.group(2).strip()
                
                current_section = {
                    "title": heading_text,
                    "content": line + "\n",
                    "level": heading_level
                }
            else:
                current_section["content"] += line + "\n"
        
        # Add final section
        if current_section["content"].strip():
            sections.append(current_section)
        
        # If no headings found, return entire content as one section
        if not sections:
            sections.append({
                "title": "Main Content",
                "content": markdown,
                "level": 1
            })
        
        return sections
    
    def _split_by_size(self, text: str, section_title: str = "") -> List[str]:
        """Split text into chunks of target size with overlap"""
        if not text.strip():
            return []
        
        # Split by paragraphs first
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        chunks = []
        current_chunk = ""
        current_tokens = 0
        
        for paragraph in paragraphs:
            paragraph_tokens = self.count_tokens(paragraph)
            
            # If single paragraph is larger than target, split it
            if paragraph_tokens > self.target_chunk_size:
                # Save current chunk if it has content
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                    current_tokens = 0
                
                # Split large paragraph by sentences
                sentences = self._split_into_sentences(paragraph)
                temp_chunk = ""
                temp_tokens = 0
                
                for sentence in sentences:
                    sentence_tokens = self.count_tokens(sentence)
                    
                    if temp_tokens + sentence_tokens > self.target_chunk_size:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                        temp_chunk = sentence + " "
                        temp_tokens = sentence_tokens
                    else:
                        temp_chunk += sentence + " "
                        temp_tokens += sentence_tokens
                
                if temp_chunk:
                    current_chunk = temp_chunk
                    current_tokens = temp_tokens
                
            # If adding paragraph would exceed target size
            elif current_tokens + paragraph_tokens > self.target_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Start new chunk with overlap from previous chunk
                overlap_text = self._get_overlap_text(current_chunk)
                current_chunk = overlap_text + "\n\n" + paragraph
                current_tokens = self.count_tokens(current_chunk)
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
                current_tokens += paragraph_tokens
        
        # Add final chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _get_overlap_text(self, text: str) -> str:
        """Get overlap text from the end of a chunk"""
        if not text:
            return ""
        
        tokens = self.encoding.encode(text)
        if len(tokens) <= self.overlap_tokens:
            return text
        
        # Get last N tokens for overlap
        overlap_tokens = tokens[-self.overlap_tokens:]
        overlap_text = self.encoding.decode(overlap_tokens)
        
        # Try to end at a sentence boundary
        sentences = overlap_text.split('.')
        if len(sentences) > 1:
            return '.'.join(sentences[1:])  # Skip partial first sentence
        
        return overlap_text
