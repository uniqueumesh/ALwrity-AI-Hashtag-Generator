import os
from typing import List, Dict, Optional
from urllib.parse import urlparse, urljoin
import re

import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup


# -------------------------------------------------------------
# ALwrity AI Hashtag Generator (Streamlit)
# -------------------------------------------------------------
# How to run:
# 1) Set your Gemini API key via environment variable GEMINI_API_KEY
#    or in Streamlit secrets as GEMINI_API_KEY
# 2) Install deps: pip install -r requirements.txt
# 3) Run: streamlit run app.py
# -------------------------------------------------------------


st.set_page_config(
    page_title="ALwrity • AI Hashtag Generator",
    page_icon="🔖",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ------------------ Platform & Category Configurations ------------------
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

# ------------------ Enhanced Prompt Template ------------------
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

# ------------------ Legacy Prompt (Fallback) ------------------
BASE_PROMPT = (
    """
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
"""
    .strip()
)


def get_api_key() -> str:
    """Read Gemini API key from Streamlit secrets or environment.
    Returns an empty string if not found.
    """
    key = ""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")  # type: ignore[attr-defined]
    except Exception:
        key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        key = os.environ.get("GEMINI_API_KEY", "")
    return key


def extract_content_from_url(url: str) -> Dict[str, str]:
    """Extract content from a given URL for hashtag generation.
    Returns a dictionary with extracted content or error message.
    """
    try:
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return {"error": "Invalid URL format"}
        
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Fetch content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        description = meta_desc.get('content', '').strip() if meta_desc else ""
        
        # Extract headings
        headings = []
        for tag in soup.find_all(['h1', 'h2', 'h3']):
            text = tag.get_text().strip()
            if text and len(text) < 200:
                headings.append(text)
        
        # Extract main content (first few paragraphs)
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 50:  # Skip short paragraphs
                paragraphs.append(text)
                if len(paragraphs) >= 3:  # Limit to first 3 substantial paragraphs
                    break
        
        # Combine extracted content
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


def get_enhanced_prompt(content: str, platform: str, category: str, num: int, source_type: str = "manual input") -> str:
    """Generate enhanced prompt based on platform and category selections."""
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
    """Adjust hashtag count based on platform optimization while respecting user preference."""
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
    """Call Gemini 2.5 model to generate a space-separated list of hashtags.
    Returns a list of cleaned, unique hashtags (length <= num).
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


def render_copy_button(text_to_copy: str) -> None:
    """Renders an in-browser copy-to-clipboard button using a small HTML snippet."""
    escaped = (
        text_to_copy.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\"", "&quot;")
        .replace("'", "&#39;")
    )
    components.html(
        f"""
<div style="display:flex;gap:0.5rem;align-items:center;">
  <textarea id="alw-hashtags" style="position:absolute;left:-9999px;top:-9999px;">{escaped}</textarea>
  <button id="alw-copy" style="
    padding:8px 14px;border-radius:10px;border:1px solid #7c3aed;
    background:linear-gradient(135deg,#7c3aed,#4f46e5);color:white;font-weight:600;cursor:pointer;"
  >Copy Hashtags</button>
</div>
<script>
  const btn = document.getElementById('alw-copy');
  const area = document.getElementById('alw-hashtags');
  btn.addEventListener('click', async () => {{
    try {{
      await navigator.clipboard.writeText(area.value);
      btn.innerText = 'Copied!';
      setTimeout(() => btn.innerText = 'Copy Hashtags', 1500);
    }} catch (err) {{
      area.select();
      document.execCommand('copy');
      btn.innerText = 'Copied!';
      setTimeout(() => btn.innerText = 'Copy Hashtags', 1500);
    }}
  }});
;</script>
        """,
        height=60,
    )


def inject_styles() -> None:
    st.markdown(
        """
<style>
/* Page background */
.stApp {{
  background: radial-gradient(1200px 600px at 10% -20%, rgba(124,58,237,0.15), transparent 40%),
              radial-gradient(1000px 500px at 110% 10%, rgba(79,70,229,0.15), transparent 40%),
              linear-gradient(180deg, #0b0f19 0%, #0b0f19 100%);
}}

/* Card container */
.alw-card {{
  border: 1px solid rgba(124,58,237,0.3);
  background: linear-gradient(180deg, rgba(17,24,39,0.9), rgba(17,24,39,0.7));
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
  border-radius: 18px;
  padding: 1.25rem;
}}

/* Big gradient title */
.alw-title {{
  font-weight: 800;
  font-size: 2.1rem;
  letter-spacing: -0.02em;
  background: linear-gradient(90deg, #a78bfa, #60a5fa);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}}

/* Subtle label */
.alw-sub {{
  color: #9ca3af;
  margin-top: -6px;
}}

/* Result tag grid */
.alw-tags {{
  display: flex; flex-wrap: wrap; gap: 8px;
}}
.alw-tag {{
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(124,58,237,0.12);
  border: 1px solid rgba(124,58,237,0.35);
  color: #e5e7eb; font-weight: 600; font-size: 0.95rem;
}}

/* Buttons */
div.stButton > button:first-child {{
  background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
  color: white !important;
  border: 1px solid #7c3aed !important;
  padding: 0.6rem 1rem !important;
  border-radius: 12px !important;
  font-weight: 700 !important;
}}

/* Text input/slider */
.stTextInput > div > div > input {{
  background: rgba(17,24,39,0.65);
  border: 1px solid rgba(124,58,237,0.35);
  border-radius: 12px;
  color: #e5e7eb;
}}
textarea {{
  background: rgba(17,24,39,0.65);
  border: 1px solid rgba(124,58,237,0.35);
  border-radius: 12px;
  color: #e5e7eb;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.95rem;
  line-height: 1.6;
  white-space: pre-wrap;
  padding: 10px 12px;
}}
</style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    inject_styles()

    with st.container():
        st.markdown("<div class='alw-card'>", unsafe_allow_html=True)

        # Content Input Section
        st.markdown("### 📝 Content Input")
        
        # Input type selection
        input_type = st.radio(
            "Choose input method:",
            ["Manual Text", "From URL"],
            horizontal=True,
            help="Enter text manually or extract content from a webpage"
        )
        
        content = ""
        source_type = "manual input"
        
        if input_type == "Manual Text":
            content = st.text_input(
                "Enter keyword or caption",
                placeholder="e.g. fitness, #contentmarketing, sustainable travel",
                help="Enter keywords, phrases, or existing captions"
            )
            source_type = "manual input"
        else:
            url_input = st.text_input(
                "Enter webpage URL",
                placeholder="e.g. https://example.com/blog-post",
                help="Paste a blog post, article, or webpage URL to extract content"
            )
            
            if url_input:
                with st.spinner("Extracting content from URL..."):
                    extracted = extract_content_from_url(url_input)
                    
                if "error" in extracted:
                    st.error(f"❌ {extracted['error']}")
                    content = ""
                else:
                    content = extracted["content"]
                    source_type = "webpage content"
                    
                    # Show extracted content preview
                    with st.expander("📄 Extracted Content Preview", expanded=False):
                        if extracted.get("title"):
                            st.write(f"**Title:** {extracted['title']}")
                        if extracted.get("description"):
                            st.write(f"**Description:** {extracted['description']}")
                        st.write(f"**Content:** {content[:300]}...")
        
        # Personalization Section
        st.markdown("### 🎯 Personalization")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            platform = st.selectbox(
                "Platform",
                ["Instagram", "TikTok", "LinkedIn", "Twitter", "YouTube"],
                help="Choose the social media platform for optimized hashtags"
            )
        
        with col2:
            category = st.selectbox(
                "Category",
                ["Business", "Lifestyle", "Technology", "Travel", "Food", "Fitness", "Education", "Entertainment"],
                help="Select content category for relevant hashtags"
            )
        
        with col3:
            user_count = st.slider("Hashtag count", min_value=5, max_value=20, value=10, step=1)
            
            # Show platform-optimized count suggestion
            optimal_count = adjust_count_for_platform(platform, user_count)
            if optimal_count != user_count:
                min_opt, max_opt = PLATFORM_CONFIG[platform]["optimal_count"]
                st.info(f"💡 {platform} works best with {min_opt}-{max_opt} hashtags")

        generate = st.button("Generate Hashtags", use_container_width=True)

        if "generated_hashtags" not in st.session_state:
            st.session_state.generated_hashtags = []  # type: ignore[attr-defined]

        if generate:
            if not content.strip():
                st.warning("Please enter content or provide a valid URL to begin.")
            else:
                # Use enhanced prompt with platform and category optimization
                enhanced_prompt = get_enhanced_prompt(content, platform, category, optimal_count, source_type)
                
                with st.spinner(f"Crafting {optimal_count} {platform}-optimized hashtags for {category} content…"):
                    try:
                        tags = generate_hashtags(content, optimal_count, enhanced_prompt)
                    except Exception as e:
                        st.error(str(e))
                        tags = []

                if tags:
                    st.session_state.generated_hashtags = tags  # type: ignore[attr-defined]
                    # Update editable text content to latest generation
                    st.session_state["hashtags_text"] = " ".join(tags)
                    
                    # Show generation info
                    st.success(f"✅ Generated {len(tags)} hashtags optimized for {platform} in {category} category")
                else:
                    st.info("No hashtags returned. Try different content or check your API key.")

        # Results area persists until next generation
        tags: List[str] = st.session_state.get("generated_hashtags", [])  # type: ignore[attr-defined]
        if tags:
            st.markdown("### 🏷️ Generated Hashtags")
            
            # Provide a single-line, space-separated version
            one_line = " ".join(tags)

            # Initialize session state if not present
            if "hashtags_text" not in st.session_state:
                st.session_state.hashtags_text = one_line

            # Single variant: editable text area for readability and tweaks
            st.text_area(
                "Generated hashtags (editable)",
                key="hashtags_text",
                height=96,
                help="You can edit these hashtags before copying them"
            )

            # Show hashtag count and platform info
            current_hashtags = st.session_state.get("hashtags_text", one_line).split()
            hashtag_count = len([h for h in current_hashtags if h.startswith('#')])
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.caption(f"📊 {hashtag_count} hashtags • Optimized for {platform} • {category} category")
            with col2:
                # Dedicated copy button (copies current edited text)
                render_copy_button(st.session_state.get("hashtags_text", one_line))

        st.markdown("</div>", unsafe_allow_html=True)  # close .alw-card

    st.markdown("\n")


if __name__ == "__main__":
    main()


