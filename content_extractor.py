"""
Content extraction utilities for ALwrity AI Hashtag Generator.
Handles URL processing and content extraction from webpages.
"""

from typing import Dict
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def extract_content_from_url(url: str) -> Dict[str, str]:
    """
    Extract content from a given URL for hashtag generation.
    
    Args:
        url (str): The URL to extract content from
        
    Returns:
        Dict[str, str]: Dictionary with extracted content or error message
    """
    try:
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return {"error": "Invalid URL format"}
        
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Fetch content with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        description = meta_desc.get('content', '').strip() if meta_desc else ""
        
        # Extract headings (h1, h2, h3)
        headings = []
        for tag in soup.find_all(['h1', 'h2', 'h3']):
            text = tag.get_text().strip()
            if text and len(text) < 200:
                headings.append(text)
        
        # Extract main content (first few substantial paragraphs)
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 50:  # Skip short paragraphs
                paragraphs.append(text)
                if len(paragraphs) >= 3:  # Limit to first 3 substantial paragraphs
                    break
        
        # Combine extracted content into a structured format
        content_parts = []
        if title_text:
            content_parts.append(f"Title: {title_text}")
        if description:
            content_parts.append(f"Description: {description}")
        if headings:
            content_parts.append(f"Key topics: {', '.join(headings[:3])}")
        if paragraphs:
            # Combine paragraphs and limit length
            combined_text = ' '.join(paragraphs)[:500] + "..."
            content_parts.append(f"Content: {combined_text}")
        
        extracted_content = ' | '.join(content_parts)
        
        return {
            "content": extracted_content,
            "title": title_text,
            "description": description,
            "url": url
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch URL: {str(e)}"}
    except Exception as e:
        return {"error": f"Error processing content: {str(e)}"}


def validate_url(url: str) -> bool:
    """
    Validate if a URL has proper format.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    try:
        parsed = urlparse(url)
        return bool(parsed.scheme and parsed.netloc)
    except Exception:
        return False
