import streamlit as st
from utils.navigation import go_to
import time

def screen_parenting_tips():

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

    st.markdown(
        "<h2 style='text-align:center'>Daily Parenting Focus</h2>",
        unsafe_allow_html=True
    )

    # Check for report
    report = st.session_state.get("full_report", {})
    tip_data = report.get("parenting_tip", {})
    
    if not tip_data:
        st.error("Tips not found. Please try again.")
        if st.button("Back to Insights"):
            go_to("insights")
        st.stop()

    # Display Tip Sections
    # 1. Responsibility
    st.markdown(
        f"""
        <div style="margin-bottom:1rem; padding:1.5rem; background:#f0f9ff; border-radius:12px; border-left: 5px solid #0ea5e9;">
            <div style="font-weight:700; color:#0369a1; margin-bottom:0.5rem; font-size:1.1rem;">🎯 Daily Responsibility</div>
            <div style="color:#334155; font-size:1.05rem; line-height:1.6;">{tip_data.get('responsibility', '')}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Appreciation
    st.markdown(
        f"""
        <div style="margin-bottom:1rem; padding:1.5rem; background:#fdf2f8; border-radius:12px; border-left: 5px solid #db2777;">
            <div style="font-weight:700; color:#be185d; margin-bottom:0.5rem; font-size:1.1rem;">❤️ Moment of Appreciation</div>
            <div style="color:#334155; font-size:1.05rem; line-height:1.6;">{tip_data.get('appreciation', '')}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. Balance Advice
    st.markdown(
        f"""
        <div style="margin-bottom:2rem; padding:1.5rem; background:#f5f3ff; border-radius:12px; border-left: 5px solid #7c3aed;">
            <div style="font-weight:700; color:#6d28d9; margin-bottom:0.5rem; font-size:1.1rem;">⚖️ Balance Advice</div>
            <div style="color:#334155; font-size:1.05rem; line-height:1.6; font-style:italic;">"{tip_data.get('balance_advice', '')}"</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Navigation
    cols = st.columns(2)
    col_back = cols[0]
    col_next = cols[1]

    with col_back:
        if st.button("← Back", key="btn_tips_back"):
            go_to("insights")

    with col_next:
        if st.button("Suggested Daily Tasks →", type="primary", key="btn_tips_to_tasks"):
            def run_tasks_logic():
                from utils.api_client import fetch_daily_tasks
                
                current_report = st.session_state.get("full_report", {})
                child_payload = st.session_state.get("child_details_payload", {})
                
                # tips is stored under 'parenting_tip' from previous step
                tips_output = current_report.get("parenting_tip", {})
                
                tasks = fetch_daily_tasks(child_payload, tips_output)
                if not tasks:
                    st.error("Failed to generate tasks.")
                    st.stop()
                    
                st.session_state["full_report"]["daily_tasks"] = tasks.get("daily_tasks", [])

            st.session_state.transition_job = {
                "title": "Creating Daily Tasks",
                "emoji": "🧩",
                "run": run_tasks_logic,
                "next": "daily_tasks",
                "context": "tasks",
            }
            go_to("transition")