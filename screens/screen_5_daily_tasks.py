import streamlit as st
from utils.navigation import go_to

def screen_daily_tasks():

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
        "<h2 style='text-align:center'>Structured Daily Micro-Tasks</h2>",
        unsafe_allow_html=True
    )

    # Check for report
    report = st.session_state.get("full_report", {})
    tasks_data = report.get("daily_tasks", [])
    
    if not tasks_data:
        st.error("No tasks found. Please try again.")
        if st.button("Back to Tips"):
            go_to("parenting_tips")
        st.stop()

    # Introduction / Reward System Info
    st.markdown(
        """
        <div style="margin-bottom:1.5rem; text-align:center; padding:1rem; background:#fff7ed; border-radius:10px; border: 1px dashed #f97316;">
            <div style="font-weight:700; color:#c2410c;">🎯 How It Works</div>
            <p style="color:#4b5563; font-size:0.9rem; margin:0.5rem 0;">Completing all 5 tasks = 1 Star ⭐<br>5 Stars = Big Reward! (Extra screen time, treat, etc.)</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Render Tasks
    icons = {
        "Discipline Task": "🟢",
        "Responsibility Task": "🟢",
        "Emotional Maturity Task": "🟢",
        "Focus Task": "🟢",
        "Confidence Task": "🟢"
    }

    for task in tasks_data:
        task_type = task.get("type", "Task")
        title = task.get("title", "Daily Mission")
        desc = task.get("description", "")
        criteria = task.get("completion_criteria", "")
        
        icon = icons.get(task_type, "🟢")

        st.markdown(
            f"""
            <div class="task-card" style="margin-bottom:1rem;">
                <div style="font-size:0.85rem; font-weight:700; color:#6b7280; text-transform:uppercase; margin-bottom:0.2rem;">
                    {icon} {task_type}
                </div>
                <div class="task-title" style="color:#1f2937; margin-bottom:0.3rem;">{title}</div>
                <div class="task-desc" style="color:#4b5563; margin-bottom:0.5rem;">{desc}</div>
                <div style="font-size:0.9rem; color:#059669; font-weight:600;">
                    ✔ {criteria}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Navigation
    if st.button("Start Daily Missions →", key="btn_start_missions"):
        st.success("✅ Tasks saved! Good luck today.")
        st.balloons()

    if st.button("← Back", key="btn_back_to_tips"):
        go_to("parenting_tips")

    st.markdown("---")

    if st.button("🔁 Start Over", key="btn_start_over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        go_to("intro")