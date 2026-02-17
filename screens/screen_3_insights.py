import streamlit as st
from utils.navigation import go_to
import time

def screen_insights():
    # Header
    st.markdown(
        """
        <div class="app-header">
            <span class="title-emoji floating-emoji">✨</span>
            <span class="app-title-text">Know Your Child</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Check if report exists
    report = st.session_state.get("full_report", None)
    
    if not report:
        st.error("No insights found. Please start over.")
        if st.button("Start Over"):
            go_to("intro")
        st.stop()



    # Sections to display
    sections = [
        ("1️⃣ Core Personality", "core_personality", "trait", "#ecfdf5", "#059669"),
        ("2️⃣ Emotional Needs", "emotional_needs", "need", "#eff6ff", "#2563eb"),
        ("3️⃣ Strengths", "strengths", "strength", "#f5f3ff", "#7c3aed"),
        ("4️⃣ Growth Areas", "growth_areas", "area", "#fff1f2", "#e11d48"),
    ]

    for title, key, item_key, bg_color, accent_color in sections:
        st.markdown(f"<h3 style='color:{accent_color}; margin-top:1.5rem; border-bottom: 2px solid {accent_color}; padding-bottom:0.5rem'>{title}</h3>", unsafe_allow_html=True)
        
        items = report.get(key, [])
        if not items:
            st.info(f"No data for {title}")
            continue
            
        for item in items:
            name = item.get(item_key, "Trait") # e.g. "Practical Thinker"
            desc = item.get("description", "")
            
            st.markdown(
                f"""
                <div style="margin-bottom:0.8rem; padding:1rem; background:{bg_color}; border-radius:10px; border-left: 4px solid {accent_color};">
                    <span style="font-weight:700; color:#1f2937; font-size:1.05rem;">{name}</span>
                    <span style="color:#6b7280; font-weight:700; margin:0 0.5rem;">–</span>
                    <span style="color:#374151; line-height:1.5;">{desc}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Navigation
    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
    cols = st.columns(2)
    
    with cols[0]:
        if st.button("← Back", key="btn_insights_back"):
            go_to("child_details")

    with cols[1]:
        if st.button("Personalize My Tips →", key="btn_insights_tips", type="primary"):
            # Next screen is tips, which we already have in full_report
            # We can use a quick transition to keep the flow feel
            st.session_state.transition_job = {
                "title": "Crafting Your Parenting Tips",
                "emoji": "👨‍👩‍👧",
                "run": lambda: time.sleep(1.5), # Fake generation time since it's pre-calculated
                "next": "parenting_tips",
                "context": "tips",
            }
            go_to("transition")
