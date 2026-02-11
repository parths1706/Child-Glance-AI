import streamlit as st
from utils.navigation import go_to

def screen_intro():

    # Brand header
    st.markdown(
        """
        <div class="app-header">
            <span class="wave-emoji">👋</span>
            <span class="app-title-text">Know Your Child</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Subtitle
    st.markdown(
        "<p class='intro-subtitle'>Every child is different. Learn what works for yours.</p>",
        unsafe_allow_html=True
    )

    # Description card
    st.markdown(
        """
        <div class="intro-card">
            <p>
            This feature helps you understand your child’s natural personality and emotional needs
            using <strong>Indian wisdom</strong> — in a simple, modern way.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Highlights
    st.markdown(
        """
        <div class="highlight-grid">
            <div class="highlight-item">🧠 <br><strong>Personality insights</strong></div>
            <div class="highlight-item">❤️ <br><strong>Emotional understanding</strong></div>
            <div class="highlight-item">👨‍👩‍👧 <br><strong>Parenting tips that work</strong></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # CTA
    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

    if st.button("✨ Get Started"):
        go_to("child_details")

    st.caption("⏱️ Takes less than 2 minutes")