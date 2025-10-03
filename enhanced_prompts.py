"""
Enhanced prompt templates for AI Hashtag Generator
Integrates Exa search data with AI prompts for better hashtag generation
"""

from typing import List, Dict, Optional


def get_enhanced_prompt_with_exa_data(
    content: str, 
    platform: str, 
    category: str, 
    num: int, 
    source_type: str = "manual input",
    exa_data: Optional[Dict] = None
) -> str:
    """
    Generate enhanced prompt with Exa search data integration
    
    Args:
        content (str): User's content
        platform (str): Target platform
        category (str): Content category
        num (int): Number of hashtags to generate
        source_type (str): Type of content source
        exa_data (Dict): Exa search results data
        
    Returns:
        str: Enhanced prompt with real-time data
    """
    
    # Base prompt template
    base_prompt = f"""
You are an expert social media strategist specializing in {platform} content.
Given the following content from {source_type}, generate exactly {num} high-quality, 
trend-aware, brand-safe hashtags optimized for {platform} in the {category} niche.

Content: "{content}"

Platform-specific requirements for {platform}:
{_get_platform_requirements(platform)}

Category focus: {category}
Include relevant terms like: {_get_category_keywords(category)}
"""

    # Add Exa data if available
    if exa_data and exa_data.get("success"):
        exa_section = _build_exa_data_section(exa_data)
        base_prompt += f"\n\n{exa_section}"
    
    # Add generation guidelines
    base_prompt += f"""

Guidelines:
- Optimize for {platform} algorithm and user behavior
- Include {category}-specific terminology
- Mix broad reach and niche targeting hashtags
- Make hashtags short (1–3 words), readable, and relevant
- Avoid duplicates, numbers, and banned/sensitive words
- Use only standard ASCII characters; no emojis
- Output as ONE single line, space-separated, each starting with '#'
- Output EXACTLY {num} hashtags and nothing else

Generate {num} hashtags:
"""
    
    return base_prompt.strip()


def _build_exa_data_section(exa_data: Dict) -> str:
    """Build Exa data section for prompt enhancement"""
    
    hashtags = exa_data.get("hashtags", [])
    trending = exa_data.get("trending", [])
    confidence = exa_data.get("confidence", 0)
    insights = exa_data.get("insights", [])
    
    section = "REAL-TIME DATA ANALYSIS:\n"
    section += f"Confidence Score: {confidence * 100:.0f}% (based on current social media trends)\n\n"
    
    if insights:
        section += "Key Insights:\n"
        for insight in insights:
            section += f"• {insight}\n"
        section += "\n"
    
    if trending:
        section += f"Currently Trending Hashtags: {', '.join(trending[:5])}\n"
        section += "Consider incorporating these trending hashtags for maximum reach.\n\n"
    
    if hashtags:
        section += f"Discovered Hashtags from Similar Content: {', '.join(hashtags[:10])}\n"
        section += "Use these as inspiration but create unique, relevant hashtags.\n\n"
    
    section += "IMPORTANT: Use the above data to inform your hashtag selection, but ensure all generated hashtags are directly relevant to the provided content."
    
    return section


def _get_platform_requirements(platform: str) -> str:
    """Get platform-specific requirements"""
    requirements = {
        "Instagram": "Focus on lifestyle, visual appeal, and community building. Include trending and evergreen hashtags.",
        "TikTok": "Emphasize trending challenges, viral content, and short catchy phrases. Include dance, music, and trend-related tags.",
        "LinkedIn": "Focus on professional development, industry insights, and thought leadership. Avoid casual or entertainment hashtags.",
        "Twitter": "Keep it minimal and news-worthy. Focus on current events, conversations, and trending topics.",
        "YouTube": "Optimize for search discovery. Include descriptive, educational, and how-to related hashtags."
    }
    return requirements.get(platform, requirements["Instagram"])


def _get_category_keywords(category: str) -> str:
    """Get category-specific keywords"""
    keywords = {
        "Business": "entrepreneur, startup, leadership, productivity, business, marketing, sales, growth",
        "Lifestyle": "dailylife, inspiration, wellness, mindfulness, lifestyle, motivation, selfcare, happiness",
        "Technology": "tech, innovation, AI, digital, software, coding, programming, future",
        "Travel": "wanderlust, adventure, explore, destination, travel, vacation, journey, discover",
        "Food": "foodie, recipe, cooking, delicious, cuisine, chef, homemade, tasty",
        "Fitness": "workout, health, motivation, fitlife, training, gym, exercise, wellness",
        "Education": "learning, knowledge, skills, growth, study, education, teaching, development",
        "Entertainment": "fun, trending, viral, creative, content, entertainment, comedy, music"
    }
    return keywords.get(category, keywords["Business"])


def get_fallback_prompt(content: str, platform: str, category: str, num: int) -> str:
    """
    Get fallback prompt when Exa data is not available
    
    Args:
        content (str): User's content
        platform (str): Target platform
        category (str): Content category
        num (int): Number of hashtags to generate
        
    Returns:
        str: Standard prompt without real-time data
    """
    return f"""
You are an expert social media strategist specializing in {platform} content.
Given the following content, generate exactly {num} high-quality, trend-aware, brand-safe hashtags optimized for {platform} in the {category} niche.

Platform-specific requirements for {platform}:
{_get_platform_requirements(platform)}

Category focus: {category}
Include relevant terms like: {_get_category_keywords(category)}

Content: "{content}"

Guidelines:
- Optimize for {platform} algorithm and user behavior
- Include {category}-specific terminology
- Mix broad reach and niche targeting hashtags
- Make hashtags short (1–3 words), readable, and relevant
- Avoid duplicates, numbers, and banned/sensitive words
- Use only standard ASCII characters; no emojis
- Output as ONE single line, space-separated, each starting with '#'
- Output EXACTLY {num} hashtags and nothing else

Generate {num} hashtags:
""".strip()
