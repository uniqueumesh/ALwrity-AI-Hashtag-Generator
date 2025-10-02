"""
Configuration settings for ALwrity AI Hashtag Generator.
Contains platform-specific settings and category keywords.
"""

# Platform-specific configurations
PLATFORM_CONFIG = {
    "Instagram": {
        "optimal_count": (8, 12),
        "style": "Mix of popular and niche hashtags for community engagement",
        "requirements": "Focus on lifestyle, visual appeal, and community building. Include trending and evergreen hashtags."
    },
    "TikTok": {
        "optimal_count": (5, 8),
        "style": "Trending and viral format hashtags",
        "requirements": "Emphasize trending challenges, viral content, and short catchy phrases. Include dance, music, and trend-related tags."
    },
    "LinkedIn": {
        "optimal_count": (3, 5),
        "style": "Professional and industry-specific hashtags",
        "requirements": "Focus on professional development, industry insights, and thought leadership. Avoid casual or entertainment hashtags."
    },
    "Twitter": {
        "optimal_count": (1, 3),
        "style": "Concise and trending topic hashtags",
        "requirements": "Keep it minimal and news-worthy. Focus on current events, conversations, and trending topics."
    },
    "YouTube": {
        "optimal_count": (5, 10),
        "style": "Searchable keyword hashtags",
        "requirements": "Optimize for search discovery. Include descriptive, educational, and how-to related hashtags."
    }
}

# Category-specific keywords for hashtag enhancement
CATEGORY_KEYWORDS = {
    "Business": ["entrepreneur", "startup", "leadership", "productivity", "business", "marketing", "sales", "growth"],
    "Lifestyle": ["dailylife", "inspiration", "wellness", "mindfulness", "lifestyle", "motivation", "selfcare", "happiness"],
    "Technology": ["tech", "innovation", "AI", "digital", "software", "coding", "programming", "future"],
    "Travel": ["wanderlust", "adventure", "explore", "destination", "travel", "vacation", "journey", "discover"],
    "Food": ["foodie", "recipe", "cooking", "delicious", "cuisine", "chef", "homemade", "tasty"],
    "Fitness": ["workout", "health", "motivation", "fitlife", "training", "gym", "exercise", "wellness"],
    "Education": ["learning", "knowledge", "skills", "growth", "study", "education", "teaching", "development"],
    "Entertainment": ["fun", "trending", "viral", "creative", "content", "entertainment", "comedy", "music"]
}

# Enhanced prompt template for AI generation
ENHANCED_PROMPT = """
You are an expert social media strategist specializing in {platform} content.
Given the following content from {source_type}, generate exactly {num} high-quality, 
trend-aware, brand-safe hashtags optimized for {platform} in the {category} niche.

Platform-specific requirements for {platform}:
{platform_requirements}

Category focus: {category}
Include relevant terms like: {category_keywords}

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
"""

# Legacy prompt for fallback
BASE_PROMPT = """
You are an expert social media strategist. Given a user seed (keyword or existing hashtag),
generate exactly {num} high-quality, trend-aware, brand-safe hashtags that would perform
well across platforms like Instagram, TikTok, LinkedIn, and X.

Guidelines:
- Make each hashtag short (1–3 words combined), readable, and relevant to the seed.
- Include a smart mix of broad and niche/long-tail hashtags for reach + intent.
- Avoid duplicates, numbers, bulleting, and any banned/sensitive words.
- Use only standard ASCII characters; no emojis.
- Output as ONE single line, space-separated, each starting with '#'.
- Output EXACTLY {num} hashtags and nothing else.

Seed: "{seed}"
""".strip()
