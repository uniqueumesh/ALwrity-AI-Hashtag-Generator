"""
UI components and styling for ALwrity AI Hashtag Generator.
Contains reusable UI functions and CSS styling for the wizard interface.
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import List, Tuple

# Import functions needed for wizard steps
from content_extractor import extract_content_from_url
from hashtag_generator import get_enhanced_prompt, adjust_count_for_platform, generate_hashtags, generate_hashtags_with_exa
from config import PLATFORM_CONFIG


def inject_styles() -> None:
    """Inject custom CSS styles for the wizard application."""
    st.markdown(
        """
<style>
/* Page background */
.stApp {
  background: radial-gradient(1200px 600px at 10% -20%, rgba(124,58,237,0.15), transparent 40%),
              radial-gradient(1000px 500px at 110% 10%, rgba(79,70,229,0.15), transparent 40%),
              linear-gradient(180deg, #0b0f19 0%, #0b0f19 100%);
}

/* Main card container */
.alw-card {
  border: 1px solid rgba(124,58,237,0.3);
  background: linear-gradient(180deg, rgba(17,24,39,0.9), rgba(17,24,39,0.7));
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
  border-radius: 18px;
  padding: 1rem;
  max-width: 700px;
  margin: 0 auto;
}

/* Enhanced buttons */
div.stButton > button:first-child {
  background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
  color: white !important;
  border: none !important;
  padding: 1rem 2rem !important;
  border-radius: 12px !important;
  font-weight: 700 !important;
  font-size: 1.1rem !important;
  box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
  transition: all 0.2s ease !important;
}

div.stButton > button:first-child:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(124,58,237,0.4) !important;
}

/* Input styling */
.stTextInput > div > div > input {
  background: rgba(15,23,42,0.8) !important;
  border: 1px solid rgba(124,58,237,0.3) !important;
  border-radius: 8px !important;
  color: #f1f5f9 !important;
  padding: 0.75rem 1rem !important;
  font-size: 1rem !important;
}

.stTextInput > div > div > input:focus {
  border-color: #7c3aed !important;
  box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}

/* Select boxes */
.stSelectbox > div > div > div {
  background: rgba(15,23,42,0.8) !important;
  border: 1px solid rgba(124,58,237,0.3) !important;
  border-radius: 8px !important;
}

/* Slider styling */
.stSlider > div > div > div > div {
  background: linear-gradient(90deg, #7c3aed, #4f46e5) !important;
  height: 6px !important;
}

/* Text area */
textarea {
  background: rgba(15,23,42,0.8) !important;
  border: 1px solid rgba(124,58,237,0.3) !important;
  border-radius: 8px !important;
  color: #f1f5f9 !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 1rem !important;
  line-height: 1.6 !important;
  padding: 1rem !important;
}

/* Success/info messages */
.stAlert {
  border-radius: 8px !important;
  border: none !important;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .alw-card {
    padding: 1rem;
    margin: 0.5rem;
  }
}
</style>
        """,
        unsafe_allow_html=True,
    )


def render_app_title() -> None:
    """Render the main application title and description."""
    # Title and description removed to make UI more compact
    pass


def render_main_container_start() -> None:
    """Render the opening of the main card container."""
    st.markdown("<div class='alw-card'>", unsafe_allow_html=True)


def render_main_container_end() -> None:
    """Render the closing of the main card container."""
    st.markdown("</div>", unsafe_allow_html=True)


def render_wizard_progress(current_step: int, total_steps: int, step_titles: List[str]) -> None:
    """Render minimal wizard progress indicator."""
    # Just show simple step dots without any container
    st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 8px; align-items: center; margin: 0.5rem 0;">
        {''.join([f'<div style="width: 8px; height: 8px; border-radius: 50%; background: {"#7c3aed" if i <= current_step else "rgba(124,58,237,0.3)"};"></div>' for i in range(1, total_steps + 1)])}
    </div>
    """, unsafe_allow_html=True)


def render_wizard_navigation(current_step: int, total_steps: int, can_proceed: bool = True, show_generate: bool = False) -> Tuple[bool, bool, bool]:
    """Render wizard navigation buttons and return button states."""
    st.markdown('<div class="wizard-navigation">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    previous_clicked = False
    next_clicked = False
    generate_clicked = False
    
    with col1:
        if current_step > 1:
            previous_clicked = st.button("← Previous", use_container_width=True, key="wizard_prev")
    
    with col3:
        if show_generate:
            generate_clicked = st.button("✨ Generate Hashtags", use_container_width=True, type="primary", key="wizard_generate")
        elif current_step < total_steps:
            next_clicked = st.button("Next →", use_container_width=True, disabled=not can_proceed, type="primary", key="wizard_next")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add navigation styling
    st.markdown("""
    <style>
    .wizard-navigation {
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(124,58,237,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    return previous_clicked, next_clicked, generate_clicked


def render_content_summary(content: str) -> None:
    """Render a summary box showing the user's content."""
    preview = content[:100] + '...' if len(content) > 100 else content
    st.markdown(f"""
    <div style="
        background: rgba(59,130,246,0.1);
        border: 1px solid rgba(59,130,246,0.3);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
    ">
        <strong style="color: #60a5fa;">📄 Your content:</strong>
        <br>
        <span style="color: #93c5fd;">{preview}</span>
    </div>
    """, unsafe_allow_html=True)


def render_settings_summary(platform: str, category: str, count: int) -> None:
    """Render a summary box showing the user's settings."""
    st.markdown(f"""
    <div style="
        background: rgba(124,58,237,0.1);
        border: 1px solid rgba(124,58,237,0.3);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
    ">
        <strong style="color: #a78bfa;">📋 Summary:</strong><br>
        <span style="color: #c4b5fd;">
            <strong>Platform:</strong> {platform} • 
            <strong>Category:</strong> {category} • 
            <strong>Count:</strong> {count} hashtags
        </span>
    </div>
    """, unsafe_allow_html=True)


def render_hashtag_results_summary(hashtag_count: int, platform: str, category: str, exa_insights: dict = None) -> None:
    """Render a success summary box for generated hashtags with Exa insights."""
    if exa_insights and exa_insights.get("success"):
        confidence = exa_insights.get("confidence", 0) * 100
        trending_count = exa_insights.get("trending_count", 0)
        
        st.markdown(f"""
        <div style="
            background: rgba(16,185,129,0.1);
            border: 1px solid rgba(16,185,129,0.3);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            text-align: center;
        ">
            <strong style="color: #10b981;">
                📊 {hashtag_count} hashtags optimized for {platform} • {category} category
            </strong>
            <br>
            <span style="color: #059669; font-size: 0.9rem;">
                🎯 {confidence:.0f}% confidence • 🔥 {trending_count} trending hashtags found
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background: rgba(16,185,129,0.1);
            border: 1px solid rgba(16,185,129,0.3);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            text-align: center;
        ">
            <strong style="color: #10b981;">
                📊 {hashtag_count} hashtags optimized for {platform} • {category} category
            </strong>
        </div>
        """, unsafe_allow_html=True)


def render_copy_button(text_to_copy: str) -> None:
    """Render an in-browser copy-to-clipboard button."""
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


def render_wizard_step_1() -> None:
    """Render Step 1: Content Input"""
    st.markdown("Choose how you want to provide your content - either type keywords directly or paste a website URL to extract content automatically.")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method",
        ["📝 Type keywords or description", "🔗 Extract from website URL"],
        horizontal=True,
        label_visibility="collapsed",
        key="wizard_input_method"
    )
    
    content = ""
    source_type = "manual input"
    
    if "📝" in input_method:
        content = st.text_input(
            "Enter your content",
            placeholder="Example: fitness motivation, healthy recipes, startup tips...",
            help="Describe your content, add keywords, or paste your caption",
            label_visibility="collapsed",
            value=st.session_state.get("wizard_content", "") if st.session_state.get("wizard_source_type") == "manual input" else "",
            key="wizard_manual_input"
        )
        source_type = "manual input"
        
    else:  # URL input
        url_input = st.text_input(
            "Enter website URL",
            placeholder="https://example.com/your-blog-post",
            help="Paste any blog post, article, or webpage URL",
            label_visibility="collapsed",
            key="wizard_url_input"
        )
        
        if url_input:
            with st.spinner("🔍 Reading content from your website..."):
                extracted = extract_content_from_url(url_input)
                
            if "error" in extracted:
                st.error(f"❌ {extracted['error']}")
                content = ""
            else:
                content = extracted["content"]
                source_type = "webpage content"
                
                # Show success message
                st.success("✅ Successfully extracted content from your website!")
                with st.expander("📄 Preview extracted content"):
                    if extracted.get("title"):
                        st.write(f"**Title:** {extracted['title']}")
                    st.write(f"**Content preview:** {content[:200]}...")
    
    # Update session state
    st.session_state["wizard_content"] = content
    st.session_state["wizard_source_type"] = source_type
    
    # Navigation
    can_proceed = bool(content.strip())
    prev_clicked, next_clicked, _ = render_wizard_navigation(1, 3, can_proceed)
    
    if next_clicked and can_proceed:
        st.session_state["wizard_step"] = 2
        st.rerun()


def render_wizard_step_2() -> None:
    """Render Step 2: Personalization"""
    st.markdown("Select your target platform and content category to get hashtags optimized for your specific needs.")
    
    # Show content summary
    render_content_summary(st.session_state.get("wizard_content", ""))
    
    # Personalization options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🎯 Platform**")
        platform = st.selectbox(
            "Select platform",
            ["Instagram", "TikTok", "LinkedIn", "Twitter", "YouTube"],
            help="Where will you post this content?",
            label_visibility="collapsed",
            index=["Instagram", "TikTok", "LinkedIn", "Twitter", "YouTube"].index(st.session_state.get("wizard_platform", "Instagram")),
            key="wizard_platform_select"
        )
    
    with col2:
        st.markdown("**📂 Category**")
        category = st.selectbox(
            "Select category",
            ["Business", "Lifestyle", "Technology", "Travel", "Food", "Fitness", "Education", "Entertainment"],
            help="What type of content is this?",
            label_visibility="collapsed",
            index=["Business", "Lifestyle", "Technology", "Travel", "Food", "Fitness", "Education", "Entertainment"].index(st.session_state.get("wizard_category", "Business")),
            key="wizard_category_select"
        )
    
    with col3:
        st.markdown("**🔢 Number of hashtags**")
        user_count = st.slider(
            "Select hashtag count",
            min_value=5, 
            max_value=20, 
            value=st.session_state.get("wizard_count", 10), 
            step=1,
            help="How many hashtags do you want?",
            label_visibility="collapsed",
            key="wizard_count_slider"
        )
    
    # Show platform optimization tip
    optimal_count = adjust_count_for_platform(platform, user_count)
    if optimal_count != user_count:
        min_opt, max_opt = PLATFORM_CONFIG[platform]["optimal_count"]
        st.info(f"💡 **Tip:** {platform} performs best with {min_opt}-{max_opt} hashtags for maximum reach!")
    
    # Update session state
    st.session_state["wizard_platform"] = platform
    st.session_state["wizard_category"] = category
    st.session_state["wizard_count"] = user_count
    
    # Navigation
    prev_clicked, next_clicked, _ = render_wizard_navigation(2, 3, True)
    
    if prev_clicked:
        st.session_state["wizard_step"] = 1
        st.rerun()
    elif next_clicked:
        st.session_state["wizard_step"] = 3
        st.rerun()


def render_wizard_step_3() -> None:
    """Render Step 3: Generate & Results"""
    
    # Show summary
    render_settings_summary(st.session_state.get("wizard_platform", "Instagram"), st.session_state.get("wizard_category", "Business"), st.session_state.get("wizard_count", 10))
    
    # Check if hashtags are already generated
    tags = st.session_state.get("generated_hashtags", [])
    
    if not tags:
        # Show generate section
        st.markdown("Click the button below to generate your personalized hashtags using AI.")
        
        # Navigation with generate button
        prev_clicked, _, generate_clicked = render_wizard_navigation(3, 3, True, show_generate=True)
        
        if prev_clicked:
            st.session_state["wizard_step"] = 2
            st.rerun()
        elif generate_clicked:
            # Generate hashtags with Exa search
            optimal_count = adjust_count_for_platform(st.session_state.get("wizard_platform", "Instagram"), st.session_state.get("wizard_count", 10))
            
            # Show enhanced loading message
            with st.spinner(f"🔍 Analyzing trends and crafting {optimal_count} {st.session_state.get('wizard_platform', 'Instagram')}-optimized hashtags for {st.session_state.get('wizard_category', 'Business')} content…"):
                try:
                    # Use Exa-enhanced generation
                    tags, exa_insights = generate_hashtags_with_exa(
                        st.session_state.get("wizard_content", ""), 
                        st.session_state.get("wizard_platform", "Instagram"), 
                        st.session_state.get("wizard_category", "Business"), 
                        optimal_count, 
                        st.session_state.get("wizard_source_type", "manual input")
                    )
                    
                    if tags:
                        st.session_state["generated_hashtags"] = tags
                        st.session_state["hashtags_text"] = " ".join(tags)
                        st.session_state.exa_insights = exa_insights
                        
                        # Show success message with confidence
                        confidence = exa_insights.get("confidence", 0) * 100
                        if exa_insights.get("success"):
                            st.success(f"✅ Generated {len(tags)} hashtags with {confidence:.0f}% confidence using real-time data")
                        else:
                            st.success(f"✅ Generated {len(tags)} hashtags using AI creativity")
                        
                        st.rerun()
                    else:
                        st.error("No hashtags returned. Try different content or check your API key.")
                except Exception as e:
                    st.error(f"Error generating hashtags: {str(e)}")
    else:
        # Show results
        st.markdown("### ✨ Your hashtags are ready!")
        
        one_line = " ".join(tags)
        
        # Initialize session state if not present
        if "hashtags_text" not in st.session_state:
            st.session_state["hashtags_text"] = one_line
        
        # Show hashtag count and platform info
        current_hashtags = st.session_state.get("hashtags_text", one_line).split()
        hashtag_count = len([h for h in current_hashtags if h.startswith('#')])
        
        exa_insights = st.session_state.get("exa_insights", {})
        render_hashtag_results_summary(hashtag_count, st.session_state.get("wizard_platform", "Instagram"), st.session_state.get("wizard_category", "Business"), exa_insights)
        
        # Editable text area
        st.markdown("**Your hashtags (you can edit them):**")
        st.text_area(
            "Edit your hashtags",
            key="hashtags_text",
            height=100,
            help="✏️ Feel free to edit, add, or remove hashtags before copying",
            label_visibility="collapsed"
        )
        
        # Copy button and restart option
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            render_copy_button(st.session_state.get("hashtags_text", one_line))
        
        st.markdown("---")
        
        # Navigation with restart option
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Previous", use_container_width=True):
                st.session_state["wizard_step"] = 2
                st.rerun()
        with col3:
            if st.button("🔄 Start Over", use_container_width=True):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    if key.startswith("wizard_") or key in ["generated_hashtags", "hashtags_text"]:
                        del st.session_state[key]
                st.session_state["wizard_step"] = 1
                st.rerun()