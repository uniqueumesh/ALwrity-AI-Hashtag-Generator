"""
Hashtag generation utilities for ALwrity AI Hashtag Generator.
Handles AI-powered hashtag generation using Google Gemini API.
"""

import os
from typing import List
import streamlit as st
import google.generativeai as genai
from config import PLATFORM_CONFIG, CATEGORY_KEYWORDS, ENHANCED_PROMPT


def get_api_key() -> str:
    """
    Read Gemini API key from Streamlit secrets or environment.
    
    Returns:
        str: API key or empty string if not found
    """
    key = ""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")  # type: ignore[attr-defined]
    except Exception:
        key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        key = os.environ.get("GEMINI_API_KEY", "")
    return key


def get_enhanced_prompt(content: str, platform: str, category: str, num: int, source_type: str = "manual input") -> str:
    """
    Generate enhanced prompt based on platform and category selections.
    
    Args:
        content (str): Content to generate hashtags for
        platform (str): Target social media platform
        category (str): Content category
        num (int): Number of hashtags to generate
        source_type (str): Type of content source
        
    Returns:
        str: Formatted prompt for AI generation
    """
    platform_info = PLATFORM_CONFIG.get(platform, PLATFORM_CONFIG["Instagram"])
    category_keywords = ", ".join(CATEGORY_KEYWORDS.get(category, []))
    
    return ENHANCED_PROMPT.format(
        platform=platform,
        source_type=source_type,
        num=num,
        category=category,
        platform_requirements=platform_info["requirements"],
        category_keywords=category_keywords,
        content=content
    )


def adjust_count_for_platform(platform: str, user_count: int) -> int:
    """
    Adjust hashtag count based on platform optimization while respecting user preference.
    
    Args:
        platform (str): Target social media platform
        user_count (int): User's preferred hashtag count
        
    Returns:
        int: Optimized hashtag count for the platform
    """
    if platform not in PLATFORM_CONFIG:
        return user_count
    
    min_count, max_count = PLATFORM_CONFIG[platform]["optimal_count"]
    
    # If user count is within optimal range, use it
    if min_count <= user_count <= max_count:
        return user_count
    
    # If user count is outside optimal range, suggest the closest optimal value
    if user_count < min_count:
        return min_count
    else:
        return max_count


def generate_hashtags(seed: str, num: int, prompt_template: str) -> List[str]:
    """
    Call Gemini 2.5 model to generate a space-separated list of hashtags.
    
    Args:
        seed (str): Content/seed for hashtag generation
        num (int): Number of hashtags to generate
        prompt_template (str): Formatted prompt template
        
    Returns:
        List[str]: List of cleaned, unique hashtags (length <= num)
    """
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "Missing GEMINI_API_KEY. Set it in environment or Streamlit secrets."
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = prompt_template.format(seed=seed.strip(), num=int(num))

    try:
        response = model.generate_content(prompt)
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(f"Gemini API error: {exc}") from exc

    text = (response.text or "").strip()
    if not text:
        return []

    # Normalize, split by whitespace, ensure leading '#', dedupe while preserving order
    raw_tokens = text.replace("\n", " ").split()
    cleaned: List[str] = []
    seen = set()
    
    for token in raw_tokens:
        tok = token.strip()
        if not tok:
            continue
        if not tok.startswith("#"):
            tok = "#" + tok.lstrip("#")
        # Keep only alphanumerics and underscores after '#'
        head, body = tok[:1], tok[1:]
        safe_body = "".join(ch for ch in body if ch.isalnum() or ch == "_")
        tok = head + safe_body
        # Skip empties or duplicates
        if len(tok) <= 1 or tok in seen:
            continue
        seen.add(tok)
        cleaned.append(tok)
        if len(cleaned) >= num:
            break

    return cleaned


def get_platform_info(platform: str) -> dict:
    """
    Get platform-specific information and settings.
    
    Args:
        platform (str): Platform name
        
    Returns:
        dict: Platform configuration dictionary
    """
    return PLATFORM_CONFIG.get(platform, PLATFORM_CONFIG["Instagram"])


def get_category_keywords(category: str) -> List[str]:
    """
    Get keywords associated with a specific category.
    
    Args:
        category (str): Category name
        
    Returns:
        List[str]: List of category-specific keywords
    """
    return CATEGORY_KEYWORDS.get(category, [])
