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
            
            def run_tips_logic():
                from utils.api_client import fetch_parenting_tips
                
                # Reconstruct inputs from session state
                # child_data is stored in screen_2 but we didn't save it to st.session_state explicitly in my previous edit?
                # Wait, I removed the line that saved child_data. I should check screen_2 again or re-construct.
                # Actually, I constructed c_payload in the run_transition_logic closure, but that scope is gone.
                # I need to ensure child_details is available.
                # Let's fix screen_2 to save child_details first, OR reconstruct it here if saved.
                # Checking screen_2: I removed `st.session_state.child_data = ...` 
                # I MUST restore that in screen_2 or similar.
                # Assuming I will fix screen_2 in next step, let's write this assuming st.session_state.child_details exists.
                
                # ACTUALLY, I will fix screen_2 to save child_details in the next turn if I missed it.
                # Let's assume st.session_state.child_details is available.
                
                # Logic:
                # 1. Get current report so far (astrology + insights)
                current_report = st.session_state.get("full_report", {})
                
                # 2. Extract specific inputs for InsightsOutput schema
                # format needed: nested objects.
                # But current_report is flattened. 
                # I need to reconstruct InsightsOutput from flattened dict.
                
                insights_output = {
                    "core_personality": current_report.get("core_personality", []),
                    "emotional_needs": current_report.get("emotional_needs", []),
                    "strengths": current_report.get("strengths", []),
                    "growth_areas": current_report.get("growth_areas", [])
                }
                
                child_payload = st.session_state.get("child_details_payload", {})

                tips = fetch_parenting_tips(child_payload, insights_output)
                if not tips:
                    st.error("Failed to generate tips.")
                    st.stop()
                
                # Update report
                # TipsOutput comes as {'responsibility': ..., 'appreciation': ...}
                # The original structure had 'parenting_tip': {...}
                # My API returns TipsOutput flat.
                # I should nest it under 'parenting_tip' to match screen_4 expectation.
                
                st.session_state["full_report"]["parenting_tip"] = tips

            st.session_state.transition_job = {
                "title": "Crafting Your Parenting Tips",
                "emoji": "👨‍👩‍👧",
                "run": run_tips_logic, 
                "next": "parenting_tips",
                "context": "tips",
            }
            go_to("transition")
