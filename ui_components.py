"""
UI components and styling for ALwrity AI Hashtag Generator.
Contains reusable UI functions and CSS styling.
"""

import streamlit as st
import streamlit.components.v1 as components


def render_copy_button(text_to_copy: str) -> None:
    """
    Renders an in-browser copy-to-clipboard button using a small HTML snippet.
    
    Args:
        text_to_copy (str): Text to copy to clipboard when button is clicked
    """
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
    """
    Inject custom CSS styles for the application.
    """
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

/* Section headers */
.section-header {{
  font-size: 1.2rem;
  font-weight: 600;
  color: #e5e7eb;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(124,58,237,0.2);
}}

/* Info boxes */
.info-box {{
  background: rgba(124,58,237,0.1);
  border: 1px solid rgba(124,58,237,0.3);
  border-radius: 8px;
  padding: 0.75rem;
  margin: 0.5rem 0;
}}

/* Success message styling */
.success-box {{
  background: rgba(34,197,94,0.1);
  border: 1px solid rgba(34,197,94,0.3);
  border-radius: 8px;
  padding: 0.75rem;
  margin: 0.5rem 0;
  color: #86efac;
}}
</style>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, icon: str = "") -> None:
    """
    Render a styled section header.
    
    Args:
        title (str): Section title
        icon (str): Optional emoji icon
    """
    st.markdown(f"### {icon} {title}")


def render_info_message(message: str, message_type: str = "info") -> None:
    """
    Render an info message with custom styling.
    
    Args:
        message (str): Message to display
        message_type (str): Type of message ('info', 'success', 'warning', 'error')
    """
    if message_type == "info":
        st.info(message)
    elif message_type == "success":
        st.success(message)
    elif message_type == "warning":
        st.warning(message)
    elif message_type == "error":
        st.error(message)


def render_hashtag_stats(hashtag_count: int, platform: str, category: str) -> None:
    """
    Render hashtag statistics and information.
    
    Args:
        hashtag_count (int): Number of hashtags
        platform (str): Target platform
        category (str): Content category
    """
    st.caption(f"📊 {hashtag_count} hashtags • Optimized for {platform} • {category} category")


def render_content_preview(extracted_data: dict) -> None:
    """
    Render extracted content preview in an expandable section.
    
    Args:
        extracted_data (dict): Dictionary containing extracted content data
    """
    with st.expander("📄 Extracted Content Preview", expanded=False):
        if extracted_data.get("title"):
            st.write(f"**Title:** {extracted_data['title']}")
        if extracted_data.get("description"):
            st.write(f"**Description:** {extracted_data['description']}")
        if extracted_data.get("content"):
            st.write(f"**Content:** {extracted_data['content'][:300]}...")


def render_platform_suggestion(platform: str, optimal_count: int, user_count: int) -> None:
    """
    Render platform optimization suggestion if needed.
    
    Args:
        platform (str): Target platform
        optimal_count (int): Optimal hashtag count for platform
        user_count (int): User's selected count
    """
    if optimal_count != user_count:
        from config import PLATFORM_CONFIG
        min_opt, max_opt = PLATFORM_CONFIG[platform]["optimal_count"]
        st.info(f"💡 {platform} works best with {min_opt}-{max_opt} hashtags")
