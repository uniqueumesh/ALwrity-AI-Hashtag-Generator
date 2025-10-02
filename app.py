"""
ALwrity AI Hashtag Generator - Main Application
A Streamlit app for generating AI-powered, platform-optimized hashtags.
"""

from typing import List
import streamlit as st

# Import custom modules
from config import PLATFORM_CONFIG
from content_extractor import extract_content_from_url
from hashtag_generator import (
    get_enhanced_prompt, 
    adjust_count_for_platform, 
    generate_hashtags
)
from ui_components import (
    inject_styles, 
    render_copy_button, 
    render_section_header,
    render_info_message,
    render_hashtag_stats,
    render_content_preview,
    render_platform_suggestion
)


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


# App configuration


# Main application logic


def main() -> None:
    """Main application function with clean, modular structure."""
    inject_styles()

    with st.container():
        st.markdown("<div class='alw-card'>", unsafe_allow_html=True)

        # Content Input Section
        render_section_header("Content Input", "📝")
        
        # Input type selection
        input_type = st.radio(
            "Choose input method:",
            ["Manual Text", "From URL"],
            horizontal=True,
            help="Enter text manually or extract content from a webpage"
        )
        
        content, source_type = handle_content_input(input_type)
        
        # Personalization Section
        render_section_header("Personalization", "🎯")
        platform, category, user_count = handle_personalization_inputs()
        
        # Generate button
        generate = st.button("Generate Hashtags", use_container_width=True)

        # Handle hashtag generation
        handle_hashtag_generation(generate, content, platform, category, user_count, source_type)

        # Display results
        display_results(platform, category)

        st.markdown("</div>", unsafe_allow_html=True)  # close .alw-card

    st.markdown("\n")


def handle_content_input(input_type: str) -> tuple[str, str]:
    """Handle content input based on user selection."""
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
                render_info_message(f"❌ {extracted['error']}", "error")
                content = ""
            else:
                content = extracted["content"]
                source_type = "webpage content"
                render_content_preview(extracted)
    
    return content, source_type


def handle_personalization_inputs() -> tuple[str, str, int]:
    """Handle personalization input controls."""
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
        
        # Show platform optimization suggestion
        optimal_count = adjust_count_for_platform(platform, user_count)
        render_platform_suggestion(platform, optimal_count, user_count)
    
    return platform, category, user_count


def handle_hashtag_generation(generate: bool, content: str, platform: str, category: str, user_count: int, source_type: str) -> None:
    """Handle the hashtag generation process."""
    if "generated_hashtags" not in st.session_state:
        st.session_state.generated_hashtags = []  # type: ignore[attr-defined]

    if generate:
        if not content.strip():
            render_info_message("Please enter content or provide a valid URL to begin.", "warning")
        else:
            optimal_count = adjust_count_for_platform(platform, user_count)
            enhanced_prompt = get_enhanced_prompt(content, platform, category, optimal_count, source_type)
            
            with st.spinner(f"Crafting {optimal_count} {platform}-optimized hashtags for {category} content…"):
                try:
                    tags = generate_hashtags(content, optimal_count, enhanced_prompt)
                except Exception as e:
                    render_info_message(str(e), "error")
                    tags = []

            if tags:
                st.session_state.generated_hashtags = tags  # type: ignore[attr-defined]
                st.session_state["hashtags_text"] = " ".join(tags)
                render_info_message(f"✅ Generated {len(tags)} hashtags optimized for {platform} in {category} category", "success")
            else:
                render_info_message("No hashtags returned. Try different content or check your API key.", "info")


def display_results(platform: str, category: str) -> None:
    """Display the generated hashtags and related controls."""
    tags: List[str] = st.session_state.get("generated_hashtags", [])  # type: ignore[attr-defined]
    if tags:
        render_section_header("Generated Hashtags", "🏷️")
        
        one_line = " ".join(tags)

        # Initialize session state if not present
        if "hashtags_text" not in st.session_state:
            st.session_state.hashtags_text = one_line

        # Editable text area
        st.text_area(
            "Generated hashtags (editable)",
            key="hashtags_text",
            height=96,
            help="You can edit these hashtags before copying them"
        )

        # Stats and copy button
        current_hashtags = st.session_state.get("hashtags_text", one_line).split()
        hashtag_count = len([h for h in current_hashtags if h.startswith('#')])
        
        col1, col2 = st.columns([2, 1])
        with col1:
            render_hashtag_stats(hashtag_count, platform, category)
        with col2:
            render_copy_button(st.session_state.get("hashtags_text", one_line))


if __name__ == "__main__":
    main()


