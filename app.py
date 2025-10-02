import os
from typing import List

import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components


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


# ------------------ Prompt (Edit to improve outputs) ------------------
# Tweak this prompt to steer hashtag quality and style.
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

        col1, col2 = st.columns([3, 1])
        with col1:
            seed = st.text_input(
                "Enter keyword or caption",
                placeholder="e.g. fitness, #contentmarketing, sustainable travel",
                
            )
        with col2:
            num = st.slider("Select number of hashtags", min_value=5, max_value=20, value=10, step=1)

        generate = st.button("Generate Hashtags", use_container_width=True)

        if "generated_hashtags" not in st.session_state:
            st.session_state.generated_hashtags = []  # type: ignore[attr-defined]

        if generate:
            if not seed.strip():
                st.warning("Please enter a keyword or hashtag to begin.")
            else:
                with st.spinner("Crafting hashtags with Gemini…"):
                    try:
                        tags = generate_hashtags(seed, num, BASE_PROMPT)
                    except Exception as e:
                        st.error(str(e))
                        tags = []

                if tags:
                    st.session_state.generated_hashtags = tags  # type: ignore[attr-defined]
                    # Update editable text content to latest generation
                    st.session_state["hashtags_text"] = " ".join(tags)
                else:
                    st.info("No hashtags returned. Try a different seed.")

        # Results area persists until next generation
        tags: List[str] = st.session_state.get("generated_hashtags", [])  # type: ignore[attr-defined]
        if tags:
            # Provide a single-line, space-separated version
            one_line = " ".join(tags)

            # Use session value when present, so user edits persist
            current_text = st.session_state.get("hashtags_text", one_line)

            # Single variant: editable text area for readability and tweaks
            st.text_area(
                "",
                value=current_text,
                key="hashtags_text",
                height=96,
                label_visibility="collapsed",
            )

            # Dedicated copy button (copies current edited text)
            render_copy_button(st.session_state.get("hashtags_text", one_line))

        st.markdown("</div>", unsafe_allow_html=True)  # close .alw-card

    st.markdown("\n")


if __name__ == "__main__":
    main()


