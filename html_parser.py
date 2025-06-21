"""
HTML Content Parser - Extracts clean content from HTML
"""
import re
from typing import Optional, Dict, Any
from readability import Document
import html2text


class HTMLParser:
    """Extracts and cleans HTML content using readability and html2text"""
    
    def __init__(self):
        self.html_converter = html2text.HTML2Text()
        self._configure_html_converter()
    
    def _configure_html_converter(self):
        """Configure html2text converter for optimal markdown output"""
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.ignore_emphasis = False
        self.html_converter.body_width = 0  # No line wrapping
        self.html_converter.protect_links = True
        self.html_converter.wrap_links = False
        
    def extract_main_content(self, html: str) -> Dict[str, Any]:
        """
        Extract main content from HTML using readability
        
        Args:
            html: Raw HTML content
            
        Returns:
            Dict containing title, cleaned HTML, and markdown
        """
        try:
            # Use readability to extract main content
            doc = Document(html)
            title = doc.title()
            clean_html = doc.summary()
            
            # Convert to markdown
            markdown = self.html_converter.handle(clean_html)
            
            # Clean up the markdown
            markdown = self._clean_markdown(markdown)
            
            return {
                "title": title,
                "html": clean_html,
                "markdown": markdown,
                "success": True
            }
            
        except Exception as e:
            # Fallback to basic HTML cleaning
            return self._fallback_extraction(html, str(e))
    
    def _clean_markdown(self, markdown: str) -> str:
        """Clean up markdown formatting"""
        # Remove excessive newlines
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        # Remove empty links
        markdown = re.sub(r'\[\]\([^)]*\)', '', markdown)
        
        # Remove excessive spaces
        markdown = re.sub(r' {2,}', ' ', markdown)
        
        # Clean up list formatting
        markdown = re.sub(r'\n\s*\*\s*\n', '\n', markdown)
        
        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in markdown.split('\n')]
        markdown = '\n'.join(lines)
        
        return markdown.strip()
    
    def _fallback_extraction(self, html: str, error: str) -> Dict[str, Any]:
        """Fallback method when readability fails"""
        try:
            # Basic HTML tag removal
            clean_html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
            clean_html = re.sub(r'<style.*?</style>', '', clean_html, flags=re.DOTALL | re.IGNORECASE)
            clean_html = re.sub(r'<nav.*?</nav>', '', clean_html, flags=re.DOTALL | re.IGNORECASE)
            clean_html = re.sub(r'<footer.*?</footer>', '', clean_html, flags=re.DOTALL | re.IGNORECASE)
            clean_html = re.sub(r'<header.*?</header>', '', clean_html, flags=re.DOTALL | re.IGNORECASE)
            
            # Convert to markdown
            markdown = self.html_converter.handle(clean_html)
            markdown = self._clean_markdown(markdown)
            
            return {
                "title": "Extracted Content",
                "html": clean_html,
                "markdown": markdown,
                "success": True,
                "fallback": True,
                "original_error": error
            }
            
        except Exception as fallback_error:
            return {
                "title": "",
                "html": "",
                "markdown": "",
                "success": False,
                "error": f"Primary error: {error}, Fallback error: {str(fallback_error)}"
            }
