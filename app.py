"""
ALwrity AI Hashtag Generator - Main Application
A Streamlit app for generating AI-powered, platform-optimized hashtags.
"""

from typing import List
import streamlit as st

# Import custom modules
# All business logic imports moved to ui_components.py for proper separation
from ui_components import (
    inject_styles, 
    render_wizard_progress,
    render_app_title,
    render_main_container_start,
    render_main_container_end,
    render_wizard_step_1,
    render_wizard_step_2,
    render_wizard_step_3
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
    """Main application function with wizard-style navigation."""
    inject_styles()

    # Initialize wizard state
    if "wizard_step" not in st.session_state:
        st.session_state.wizard_step = 1
    if "wizard_content" not in st.session_state:
        st.session_state.wizard_content = ""
    if "wizard_source_type" not in st.session_state:
        st.session_state.wizard_source_type = "manual input"
    if "wizard_platform" not in st.session_state:
        st.session_state.wizard_platform = "Instagram"
    if "wizard_category" not in st.session_state:
        st.session_state.wizard_category = "Business"
    if "wizard_count" not in st.session_state:
        st.session_state.wizard_count = 10

    # App title and description
    render_app_title()

    with st.container():
        render_main_container_start()

        # Step titles for wizard
        step_titles = [
            "What do you want hashtags for?",
            "Customize for your needs",
            "Generate & Results"
        ]

        # Render wizard progress
        render_wizard_progress(st.session_state.wizard_step, 3, step_titles)

        # Render current step content
        if st.session_state.wizard_step == 1:
            render_wizard_step_1()
        elif st.session_state.wizard_step == 2:
            render_wizard_step_2()
        elif st.session_state.wizard_step == 3:
            render_wizard_step_3()

        render_main_container_end()  # close .alw-card


# Wizard step functions moved to ui_components.py for proper separation


# Legacy functions removed - wizard implementation handles all functionality


if __name__ == "__main__":
    main()


